# (generated with --quick)

import gymnasium as gym
import numpy as np
import rllte.env.utils
from typing import Any, Type

AsyncVectorEnv: Any
FlatObsWrapper: Any
FrameStack: Type[rllte.env.utils.FrameStack]
FullyObsWrapper: Any
RecordEpisodeStatistics: Any
SyncVectorEnv: Any
TorchVecEnvWrapper: Type[rllte.env.utils.TorchVecEnvWrapper]

class Minigrid2Image(Any):
    __doc__: str
    observation_space: Any
    def __init__(self, env) -> None: ...
    def observation(self, observation: dict) -> np.ndarray: ...

def make_minigrid_env(env_id: str = ..., num_envs: int = ..., fully_observable: bool = ..., seed: int = ..., frame_stack: int = ..., device: str = ..., distributed: bool = ...) -> Any: ...
