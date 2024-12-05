from collections.abc import Callable

import numpy

def get_union_keys(left: VectorDict, right: VectorDict): ...
def get_intersection_keys(left: VectorDict, right: VectorDict): ...

class VectorDict:
    def __init__(
        self,
        data: VectorDict | dict | None = None,
        default_factory: Callable | None = None,
        mask: VectorDict | set | None = None,
        copy: bool = False,
    ) -> None: ...
    def with_mask(self, mask, copy=False): ...
    def to_dict(self): ...
    def to_numpy(self, fields) -> numpy.ndarray: ...
    def __contains__(self, key): ...
    def __delitem__(self, key): ...
    def __format__(self, format_spec): ...
    def __getitem__(self, key): ...
    def __iter__(self): ...
    def __len__(self): ...
    def __repr__(self): ...
    def __setitem__(self, key, value): ...
    def __str__(self): ...
    def clear(self): ...
    def get(self, key, *args, **kwargs): ...
    def items(self): ...
    def keys(self): ...
    def pop(self, *args, **kwargs): ...
    def popitem(self): ...
    def setdefault(self, key, *args, **kwargs): ...
    def update(self, *args, **kwargs): ...
    def values(self): ...
    def __eq__(left, right): ...
    def __add__(left, right): ...
    def __iadd__(self, other): ...
    def __sub__(left, right): ...
    def __isub__(self, other): ...
    def __mul__(left, right): ...
    def __imul__(self, other): ...
    def __truediv__(left, right): ...
    def __itruediv__(self, other): ...
    def __pow__(left, right): ...
    def __ipow__(self, other): ...
    def __matmul__(left, right): ...
    def __neg__(self): ...
    def __pos__(self): ...
    def __abs__(self): ...
    def abs(self): ...
    def min(self): ...
    def max(self): ...
    def minimum(self, other): ...
    def maximum(self, other): ...
