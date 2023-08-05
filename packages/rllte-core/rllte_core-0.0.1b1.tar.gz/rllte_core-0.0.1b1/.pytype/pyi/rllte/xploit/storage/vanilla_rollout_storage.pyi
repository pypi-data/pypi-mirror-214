# (generated with --quick)

import gymnasium as gym
import rllte.common.base_storage
import torch as th
from typing import Any, Type

BaseStorage: Type[rllte.common.base_storage.BaseStorage]
BatchSampler: Any
SubsetRandomSampler: Any

class VanillaRolloutStorage(rllte.common.base_storage.BaseStorage):
    __doc__: str
    actions: Any
    advantages: Any
    batch_size: int
    discount: float
    gae_lambda: float
    global_step: int
    log_probs: Any
    num_envs: int
    num_steps: int
    obs: Any
    returns: Any
    rewards: Any
    terminateds: Any
    truncateds: Any
    values: Any
    def __init__(self, observation_space, action_space, device: str = ..., num_steps: int = ..., num_envs: int = ..., batch_size: int = ..., discount: float = ..., gae_lambda: float = ...) -> None: ...
    def add(self, obs, actions, rewards, terminateds, truncateds, next_obs, log_probs, values) -> None: ...
    def compute_returns_and_advantages(self, last_values) -> None: ...
    def sample(self) -> generator: ...
    def update(self) -> None: ...
