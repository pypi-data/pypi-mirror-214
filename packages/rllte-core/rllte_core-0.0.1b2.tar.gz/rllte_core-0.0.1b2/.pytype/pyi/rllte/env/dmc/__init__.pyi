# (generated with --quick)

import gymnasium as gym
import numpy as np
import rllte.env.dmc.wrappers
import rllte.env.utils
from dm_control import manipulation
from dm_control import suite
from dm_control.suite.wrappers import action_scale
from dm_control.suite.wrappers import pixels
from typing import Any, Type

ActionDTypeWrapper: Type[rllte.env.dmc.wrappers.ActionDTypeWrapper]
ActionRepeatWrapper: Type[rllte.env.dmc.wrappers.ActionRepeatWrapper]
DMC2Gymnasium: Type[rllte.env.dmc.wrappers.DMC2Gymnasium]
FlatObsWrapper: Type[rllte.env.dmc.wrappers.FlatObsWrapper]
FrameStackWrapper: Type[rllte.env.dmc.wrappers.FrameStackWrapper]
RecordEpisodeStatistics: Any
SyncVectorEnv: Any
TorchVecEnvWrapper: Type[rllte.env.utils.TorchVecEnvWrapper]

def make_dmc_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., visualize_reward: bool = ..., from_pixels: bool = ..., height: int = ..., width: int = ..., frame_stack: int = ..., action_repeat: int = ...) -> Any: ...
