import numpy as np
import torch as t
from torch import nn
from torch.utils.data import Dataset
import numpy as np
from fancy_einsum import einsum
from dataclasses import dataclass
import functools


from einops import rearrange, reduce, repeat

@dataclass(frozen=True)
class TransformerConfig:
    '''Constants used throughout the decoder-only transformer model.'''

    num_layers: int
    num_heads: int
    vocab_size: int
    hidden_size: int
    max_seq_len: int
    dropout: float = 0.1
    layer_norm_epsilon: float = 1e-05

class WordsDataset(Dataset):
    def __init__(self, seq_len, filename, tokenizer, truncate=None):
        self.seq_len = seq_len
        self.filename = filename
        
        with open(filename, 'r') as textfile:
            text = textfile.read()
        
        tokenizer.build_dict(text)
        self.tokens = tokenizer.encode(text)
        
        word_count = len(self.tokens)

        if truncate:
            word_count = int(word_count * truncate)

        self.x_seqs, self.y_seqs = [], []
        
        for pos in range(0, word_count - seq_len - 1):
            self.x_seqs.append(t.tensor(self.tokens[pos:pos+self.seq_len]))
            self.y_seqs.append(t.tensor(self.tokens[pos+1:pos+self.seq_len+1]))
        self.x_seqs = t.stack(self.x_seqs)
        self.y_seqs = t.stack(self.y_seqs)

    def __len__(self):
        return len(self.x_seqs)

    def __getitem__(self, idx):
        return self.x_seqs[idx], self.y_seqs[idx]