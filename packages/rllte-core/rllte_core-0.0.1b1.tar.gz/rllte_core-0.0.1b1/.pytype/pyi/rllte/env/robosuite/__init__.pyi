# (generated with --quick)

import gymnasium as gym
import numpy as np
import rllte.env.utils
import robosuite as suite
from typing import Any, Tuple, Type

AsyncVectorEnv: Any
GymWrapper: Any
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

def make_robosuite_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., distributed: bool = ..., has_renderer: bool = ..., has_offscreen_renderer: bool = ..., use_camera_obs: bool = ...) -> Any: ...
