# (generated with --quick)

import gymnasium as gym
import numpy as np
import rllte.common.base_storage
import torch as th
from typing import Any, Type

BaseStorage: Type[rllte.common.base_storage.BaseStorage]

class VanillaReplayStorage(rllte.common.base_storage.BaseStorage):
    __doc__: str
    actions: Any
    batch_size: int
    full: bool
    global_step: int
    obs: Any
    rewards: Any
    storage_size: int
    terminateds: Any
    truncateds: Any
    def __init__(self, observation_space, action_space, device: str = ..., storage_size: int = ..., batch_size: int = ...) -> None: ...
    def __len__(self) -> int: ...
    def add(self, obs, action, reward, terminated, truncated, info, next_obs) -> None: ...
    def sample(self, step: int) -> tuple: ...
    def update(self, *args) -> None: ...
