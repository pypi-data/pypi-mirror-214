# (generated with --quick)

import numpy as np
import rllte.common.base_distribution
import torch as th
from rllte.xplore.distribution import utils
from typing import Annotated, Any, Type

BaseDistribution: Type[rllte.common.base_distribution.BaseDistribution]
_standard_normal: Any

class OrnsteinUhlenbeckNoise(rllte.common.base_distribution.BaseDistribution):
    __doc__: str
    dt: float
    eps: float
    high: float
    loc: float
    low: float
    mean: Annotated[Any, 'property']
    mode: Annotated[Any, 'property']
    noise_prev: Any
    noiseless_action: Any
    scale: float
    stddev: Annotated[Any, 'property']
    stddev_clip: float
    stddev_schedule: str
    theta: float
    variance: Annotated[Any, 'property']
    def __init__(self, loc: float = ..., scale: float = ..., low: float = ..., high: float = ..., eps: float = ..., theta: float = ..., dt: float = ..., stddev_schedule: str = ..., stddev_clip: float = ...) -> None: ...
    def _clamp(self, x) -> Any: ...
    def entropy(self) -> Any: ...
    def log_prob(self, value) -> Any: ...
    def reset(self, noiseless_action, step: int = ...) -> None: ...
    def rsample(self, sample_shape = ...) -> Any: ...
    def sample(self, clip: bool = ..., sample_shape = ...) -> Any: ...
