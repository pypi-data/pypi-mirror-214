# (generated with --quick)

import gymnasium as gym
from torch import nn
from typing import Any

class BaseEncoder(Any):
    __doc__: str
    feature_dim: int
    observation_space: Any
    def __init__(self, observation_space, feature_dim: int = ...) -> None: ...
