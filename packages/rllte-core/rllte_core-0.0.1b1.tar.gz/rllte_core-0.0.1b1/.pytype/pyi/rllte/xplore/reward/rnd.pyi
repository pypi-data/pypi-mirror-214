# (generated with --quick)

import gymnasium as gym
import numpy as np
import rllte.common.base_reward
import torch as th
from torch import nn
from torch.nn import functional as F
from typing import Any, Type

BaseIntrinsicRewardModule: Type[rllte.common.base_reward.BaseIntrinsicRewardModule]
DataLoader: Any
TensorDataset: Any

class Encoder(Any):
    __doc__: str
    linear: Any
    trunk: Any
    def __init__(self, obs_shape: tuple, action_dim: int, latent_dim: int) -> None: ...
    def forward(self, obs) -> Any: ...

class RND(rllte.common.base_reward.BaseIntrinsicRewardModule):
    __doc__: str
    batch_size: int
    opt: Any
    predictor: Any
    target: Any
    def __init__(self, observation_space, action_space, device: str = ..., beta: float = ..., kappa: float = ..., latent_dim: int = ..., lr: float = ..., batch_size: int = ...) -> None: ...
    def compute_irs(self, samples: dict, step: int = ...) -> Any: ...
    def update(self, samples: dict) -> None: ...
