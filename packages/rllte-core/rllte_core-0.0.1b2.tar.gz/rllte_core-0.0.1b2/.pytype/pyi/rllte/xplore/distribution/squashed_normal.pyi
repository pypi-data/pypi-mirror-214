# (generated with --quick)

import math
import rllte.common.base_distribution
import torch as th
from torch import distributions as pyd
from torch.nn import functional as F
from typing import Annotated, Any, Type

BaseDistribution: Type[rllte.common.base_distribution.BaseDistribution]

class SquashedNormal(rllte.common.base_distribution.BaseDistribution):
    __doc__: str
    dist: Any
    loc: Any
    mean: Annotated[Any, 'property']
    mode: Annotated[Any, 'property']
    scale: Any
    stddev: Annotated[Any, 'property']
    variance: Annotated[Any, 'property']
    def __init__(self, loc, scale) -> None: ...
    def entropy(self) -> Any: ...
    def log_prob(self, actions) -> Any: ...
    def reset(self) -> None: ...
    def rsample(self, sample_shape = ...) -> Any: ...
    def sample(self, sample_shape = ...) -> Any: ...

class TanhTransform(Any):
    __doc__: str
    bijective: bool
    codomain: Any
    domain: Any
    sign: int
    def __eq__(self, other) -> bool: ...
    def __init__(self, cache_size = ...) -> None: ...
    def _call(self, x) -> Any: ...
    def _inverse(self, y) -> Any: ...
    @staticmethod
    def atanh(x) -> Any: ...
    def log_abs_det_jacobian(self, x, y) -> Any: ...
