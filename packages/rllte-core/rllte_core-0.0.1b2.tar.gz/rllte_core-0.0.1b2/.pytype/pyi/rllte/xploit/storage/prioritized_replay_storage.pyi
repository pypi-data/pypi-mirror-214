# (generated with --quick)

import collections
import gymnasium as gym
import numpy as np
import rllte.common.base_storage
import torch as th
from typing import Any, Dict, Type

BaseStorage: Type[rllte.common.base_storage.BaseStorage]
deque: Type[collections.deque]

class PrioritizedReplayStorage(rllte.common.base_storage.BaseStorage):
    __doc__: str
    alpha: float
    batch_size: int
    beta: float
    position: int
    priorities: Any
    storage: collections.deque
    storage_size: int
    def __init__(self, observation_space, action_space, device: str = ..., storage_size: int = ..., batch_size: int = ..., alpha: float = ..., beta: float = ...) -> None: ...
    def __len__(self) -> int: ...
    def add(self, obs: np.ndarray, action: np.ndarray, reward: np.ndarray, terminated: np.ndarray, truncated: np.ndarray, info: Dict[str, Any], next_obs: np.ndarray) -> None: ...
    def annealing_beta(self, step: int) -> float: ...
    def sample(self, step: int) -> tuple: ...
    def update(self, metrics: dict) -> None: ...
