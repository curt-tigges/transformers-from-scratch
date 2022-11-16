import numpy as np
import torch as t
from torch import nn
import numpy as np
from fancy_einsum import einsum
from dataclasses import dataclass

from einops import rearrange, reduce, repeat

import general_modules as cm

@dataclass(frozen=True)
class TransformerConfig:
    '''Constants used throughout your decoder-only transformer model.'''

    num_layers: int
    num_heads: int
    vocab_size: int
    hidden_size: int
    max_seq_len: int
    dropout: float = 0.1
    layer_norm_epsilon: float = 1e-05

class Embedding(nn.Module):
    """Returns an embedding of input tokens"""

    def __init__(self, num_embeddings: int, embedding_dim: int):
        super().__init__()
        self.num_embed = num_embeddings
        self.embed_dim = embedding_dim
        self.weight = nn.Parameter(
            t.ones(num_embeddings, embedding_dim).uniform_(-1, to=1)
        )

    def forward(self, x: t.LongTensor) -> t.Tensor:
        """For each integer in the input, return that row of the embedding."""
        return self.weight[x]

    def extra_repr(self) -> str:
        return f"{self.num_embed}, {self.embed_dim}"


class PositionalEncoding(nn.Module):
    """Adds sin-cosine positional encoding to the input"""

    def __init__(self, max_seq_len: int, embedding_dim: int):
        super().__init__()
        self.max_seq_len = max_seq_len
        self.embed_dim = embedding_dim
        self.n = 10000

        freqs = np.outer(
            np.arange(max_seq_len),
            1 / self.n ** (2 * np.arange(embedding_dim // 2) / embedding_dim),
        )
        enc_2d = np.zeros((max_seq_len, embedding_dim))
        enc_2d[:, ::2] = np.sin(freqs)
        enc_2d[:, 1::2] = np.cos(freqs)
        self.register_buffer("pos_enc", t.from_numpy(enc_2d))

    def forward(self, x: t.Tensor) -> t.Tensor:
        """
        x: shape (batch, seq_len, embedding_dim)
        """
        return x + self.pos_enc[: x.shape[1], :]

    def extra_repr(self) -> str:
        return f"max_freq={self.n}, max_seq_len={self.max_seq_len}, embedding_dim={self.embed_dim}"


class LayerNorm(nn.Module):
    """Performs normalization over specified dimensions"""

    def __init__(
        self, normalized_shape, eps: float = 1e-05, elementwise_affine: bool = True
    ):
        super().__init__()
        self.norm_shape = (
            (normalized_shape,)
            if isinstance(normalized_shape, int)
            else normalized_shape
        )
        self.eps = eps
        self.elementwise_affine = elementwise_affine

        if self.elementwise_affine:
            self.weight = nn.Parameter(t.ones(normalized_shape))
            self.bias = nn.Parameter(t.zeros(normalized_shape))

    def forward(self, x: t.Tensor) -> t.Tensor:
        """Normalize along each embedding"""
        x_dims, norm_shape_dims = len(x.shape), len(self.norm_shape)
        norm_dims = tuple([d for d in range(x_dims - norm_shape_dims, x_dims)])

        self.mean = t.mean(x, dim=norm_dims, keepdim=True)
        self.var = t.var(x, dim=norm_dims, unbiased=False, keepdim=True)

        out = (x - self.mean) / t.sqrt(self.var + self.eps)

        if self.elementwise_affine:
            out = out * self.weight + self.bias

        return out

    def extra_repr(self) -> str:
        return f"normalized_shape={self.norm_shape}, eps={self.eps}, elementwise_affine={self.elementwise_affine}"


class Dropout(nn.Module):
    """Returns activations to which the Dropout technique has been applied"""

    def __init__(self, p: float):
        super().__init__()
        self.p = p

    def forward(self, x: t.Tensor) -> t.Tensor:
        if self.training:
            d_shape = x.shape
            dropout_matrix = t.rand(d_shape)
            dropout_matrix[dropout_matrix < self.p] = 0
            dropout_matrix[dropout_matrix >= self.p] = 1
            # should this be on the device?
            out = x * dropout_matrix.to(x.device)
            out = out / (1 - self.p)
            return out
        else:
            return x

    def extra_repr(self) -> str:
        return f"p={self.p}"


class GELU(nn.Module):
    """Performs the GELU approximation"""

    def forward(self, x: t.Tensor) -> t.Tensor:
        out = (
            x * 0.5 * (1 + t.tanh(t.sqrt(t.tensor(2 / t.pi)) * (x + 0.044715 * x**3)))
        )
        return out


class MultiheadMaskedAttention(nn.Module):
    W_QKV: nn.Linear
    W_O: nn.Linear

    def __init__(self, hidden_size: int, num_heads: int):
        super().__init__()
        self.num_heads = num_heads
        self.query_size = int(hidden_size / num_heads)
        self.qkv = cm.Linear(hidden_size, 3 * hidden_size)
        self.ff = cm.Linear(hidden_size, hidden_size)

    def multihead_masked_attention(
        self, Q: t.Tensor, K: t.Tensor, V: t.Tensor, num_heads: int
    ):
        """
        Implements multihead masked attention on the matrices Q, K and V.

        Q: shape (batch, seq, nheads*headsize)
        K: shape (batch, seq, nheads*headsize)
        V: shape (batch, seq, nheads*headsize)

        returns: shape (batch, seq, nheads*headsize)
        """
        Q = rearrange(
            Q, "B S (nheads headsize) -> B S nheads headsize", nheads=num_heads
        )
        K = rearrange(
            K, "B S (nheads headsize) -> B S nheads headsize", nheads=num_heads
        )
        V = rearrange(
            V, "B S (nheads headsize) -> B S nheads headsize", nheads=num_heads
        )

        batch_size, seq_len, nheads, headsize = Q.shape
        scores = einsum(
            "B Qseq nheads headsize, B Kseq nheads headsize -> B nheads Qseq Kseq", Q, K
        )
        scores /= Q.shape[-1] ** 0.5

        # create lower-left triangle of ones, including the diagonal
        mask = t.tril(t.ones(seq_len, seq_len).to(Q.device), diagonal=0)
        #mask = mask.to(Q.device)
        # fill with close-to-neg-inf values where mask==0
        #print(mask.device)
        #print(scores.device)
        scores = scores.masked_fill(mask == 0, -1e9)

        scores = t.softmax(scores, dim=-1)
        Z = einsum(
            "B nheads Qseq Kseq, B Kseq nheads headsize -> B Qseq nheads headsize",
            scores,
            V,
        )
        Z = rearrange(Z, "B Qseq nheads headsize -> B Qseq (nheads headsize)")
        return Z

    def forward(self, x: t.Tensor) -> t.Tensor:
        """
        x: shape (batch, seq, hidden_size)

        Return: shape (batch, seq, hidden_size)
        """
        out = self.qkv(x)
        Q, K, V = t.tensor_split(out, 3, dim=-1)

        Z = self.multihead_masked_attention(Q, K, V, self.num_heads)
        out = self.ff(Z)
        return out


class MLP(nn.Module):
    def __init__(self, hidden_size, dropout):
        super().__init__()
        self.linear1 = cm.Linear(hidden_size, 4 * hidden_size)
        self.gelu = GELU()
        self.linear2 = cm.Linear(4 * hidden_size, hidden_size)
        self.dropout = Dropout(p=dropout)

    def forward(self, x):
        out = self.gelu(self.linear1(x))
        out = self.dropout(self.linear2(out))
        return out

class DecoderBlock(nn.Module):

    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.attn = MultiheadMaskedAttention(config.hidden_size, config.num_heads)
        self.lnorm1 = LayerNorm(config.hidden_size, eps=config.layer_norm_epsilon)
        self.mlp = MLP(config.hidden_size, config.dropout)
        self.lnorm2 = LayerNorm(config.hidden_size, eps=config.layer_norm_epsilon)

    def forward(self, x: t.Tensor) -> t.Tensor:
        normed_attn = self.lnorm1(self.attn(x))
        out = normed_attn + x
        normed_mlp = self.lnorm2(self.mlp(out))
        out = normed_mlp + out
        return out

class DecoderOnlyTransformer(nn.Module):

    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.emb = Embedding(config.vocab_size, config.hidden_size)
        self.pos_enc = PositionalEncoding(config.max_seq_len, config.hidden_size)
        self.dropout = Dropout(p=config.dropout)

        decoders = [DecoderBlock(config) for l in range(config.num_layers)]
        self.decoders = nn.Sequential(*decoders)
        
        self.post_norm = LayerNorm(config.hidden_size)

    def forward(self, x: t.Tensor) -> t.Tensor:
        embedding = self.emb(x.long())
        embedding = self.pos_enc(embedding)
        embedding = self.dropout(embedding)
        embedding = embedding.to(t.float32)

        out = self.decoders(embedding)
        out = self.post_norm(out)

        out = einsum("B S E, V E -> B S V", out, self.emb.weight)

        return out