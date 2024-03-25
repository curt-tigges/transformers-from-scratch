import numpy as np
from fancy_einsum import einsum
from einops import reduce, rearrange, repeat
from typing import Union, Optional, Callable
import torch as t
import functools
from torch import nn


class ReLU(nn.Module):
    def forward(self, x: t.Tensor) -> t.Tensor:
        return t.maximum(x, t.tensor(0.0))


class Flatten(nn.Module):
    def __init__(self, start_dim: int = 1, end_dim: int = -1) -> None:
        super().__init__()
        self.start_dim = start_dim
        self.end_dim = end_dim

    def forward(self, input: t.Tensor) -> t.Tensor:
        """Flatten out dimensions from start_dim to end_dim, inclusive of both."""
        t_dims = input.shape
        end = self.end_dim if self.end_dim >= 0 else len(t_dims) + self.end_dim
        flattened_size = functools.reduce(
            lambda x, y: x * y, t_dims[self.start_dim : end + 1]
        )

        new_shape = t_dims[: self.start_dim] + (flattened_size,) + t_dims[end + 1 :]

        return t.reshape(input, new_shape)

    def extra_repr(self) -> str:
        return f"Reshapes from dim {self.start_dim} to {self.end_dim} inclusive"


class Linear(nn.Module):
    def __init__(self, in_features: int, out_features: int, bias=True):
        """A simple linear (technically, affine) transformation.
        """
        super().__init__()
        k = 1 / np.sqrt(in_features)

        self.weight = nn.Parameter(
            t.zeros(out_features, in_features).uniform_(-k, to=k)
        )
        self.bias = (
            None if not bias else nn.Parameter(t.zeros(out_features).uniform_(-k, to=k))
        )

    def forward(self, x: t.Tensor) -> t.Tensor:
        """
        x: shape (*, in_features)
        Return: shape (*, out_features)
        """
        out = einsum("... in_f, out_f in_f -> ... out_f", x, self.weight)
        if self.bias != None:
            out += self.bias

        return out

    def extra_repr(self) -> str:
        pass
