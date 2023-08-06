# (generated with --quick)

import gymnasium as gym
import numpy as np
import rllte.env.utils
from typing import Any, Dict, Optional, SupportsFloat, Tuple, Type

AsyncVectorEnv: Any
RecordEpisodeStatistics: Any
SyncVectorEnv: Any
TorchVecEnvWrapper: Type[rllte.env.utils.TorchVecEnvWrapper]

class PixelEnv(Any):
    __doc__: str
    action_space: Any
    observation_space: Any
    def __init__(self) -> None: ...
    def reset(self, seed: Optional[int] = ..., options = ...) -> Tuple[Any, Dict[str, Any]]: ...
    def step(self, action) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]: ...

class StateEnv(Any):
    __doc__: str
    action_space: Any
    observation_space: Any
    def __init__(self) -> None: ...
    def reset(self, seed: Optional[int] = ..., options = ...) -> Tuple[Any, Dict[str, Any]]: ...
    def step(self, action) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]: ...

def make_multibinary_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., distributed: bool = ...) -> Any: ...
