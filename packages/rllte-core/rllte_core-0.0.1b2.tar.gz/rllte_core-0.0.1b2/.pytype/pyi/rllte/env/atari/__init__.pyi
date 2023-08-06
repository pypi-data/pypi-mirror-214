# (generated with --quick)

import gymnasium as gym
import numpy as np
import rllte.env.atari.wrappers
import rllte.env.utils
from typing import Any, Type

AsyncVectorEnv: Any
EpisodicLifeEnv: Type[rllte.env.atari.wrappers.EpisodicLifeEnv]
FireResetEnv: Type[rllte.env.atari.wrappers.FireResetEnv]
FrameStack: Any
GrayScaleObservation: Any
MaxAndSkipEnv: Type[rllte.env.atari.wrappers.MaxAndSkipEnv]
NoopResetEnv: Type[rllte.env.atari.wrappers.NoopResetEnv]
RecordEpisodeStatistics: Any
ResizeObservation: Any
SyncVectorEnv: Any
TorchVecEnvWrapper: Type[rllte.env.utils.TorchVecEnvWrapper]
TransformReward: Any

def make_atari_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., frame_stack: int = ..., distributed: bool = ...) -> Any: ...
