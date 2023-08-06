# (generated with --quick)

import gymnasium as gym
import rllte.common.base_encoder
import torch as th
from torch import nn
from typing import Any, Type

BaseEncoder: Type[rllte.common.base_encoder.BaseEncoder]

class MnihCnnEncoder(rllte.common.base_encoder.BaseEncoder):
    __doc__: str
    trunk: Any
    def __init__(self, observation_space, feature_dim: int = ...) -> None: ...
    def forward(self, obs) -> Any: ...
