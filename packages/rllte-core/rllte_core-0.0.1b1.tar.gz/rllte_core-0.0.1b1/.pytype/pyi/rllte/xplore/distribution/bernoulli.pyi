# (generated with --quick)

import rllte.common.base_distribution
import torch as th
from torch import distributions as pyd
from typing import Annotated, Any, Type

BaseDistribution: Type[rllte.common.base_distribution.BaseDistribution]

class Bernoulli(rllte.common.base_distribution.BaseDistribution):
    __doc__: str
    dist: Any
    logits: Annotated[Any, 'property']
    mean: Annotated[Any, 'property']
    mode: Annotated[Any, 'property']
    probs: Annotated[Any, 'property']
    stddev: Annotated[Any, 'property']
    variance: Annotated[Any, 'property']
    def __init__(self, logits) -> None: ...
    def entropy(self) -> Any: ...
    def log_prob(self, actions) -> Any: ...
    def reset(self) -> None: ...
    def rsample(self, sample_shape = ...) -> Any: ...
    def sample(self, sample_shape = ...) -> Any: ...
