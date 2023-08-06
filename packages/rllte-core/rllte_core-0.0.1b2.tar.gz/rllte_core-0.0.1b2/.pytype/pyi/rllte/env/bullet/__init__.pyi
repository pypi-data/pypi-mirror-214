# (generated with --quick)

import gym as old_gym
import gymnasium as gym
import numpy as np
import pybullet_envs
import rllte.env.utils
from typing import Any, Tuple, Type

AsyncVectorEnv: Any
RecordEpisodeStatistics: Any
SyncVectorEnv: Any
TorchVecEnvWrapper: Type[rllte.env.utils.TorchVecEnvWrapper]

class AdapterEnv(Any):
    __doc__: str
    action_space: Any
    observation_space: Any
    def __init__(self, env) -> None: ...
    def reset(self, **kwargs) -> Tuple[np.ndarray, dict]: ...
    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, bool, dict]: ...

def make_bullet_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., distributed: bool = ...) -> Any: ...
