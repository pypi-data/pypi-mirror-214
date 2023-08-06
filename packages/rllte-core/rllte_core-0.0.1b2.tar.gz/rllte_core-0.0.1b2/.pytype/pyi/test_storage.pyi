# (generated with --quick)

import pytest
import rllte.xploit.storage.nstep_replay_storage
import rllte.xploit.storage.prioritized_replay_storage
import rllte.xploit.storage.vanilla_replay_storage
import rllte.xploit.storage.vanilla_rollout_storage
import torch as th
from typing import Any, Type

NStepReplayStorage: Type[rllte.xploit.storage.nstep_replay_storage.NStepReplayStorage]
PrioritizedReplayStorage: Type[rllte.xploit.storage.prioritized_replay_storage.PrioritizedReplayStorage]
VanillaReplayStorage: Type[rllte.xploit.storage.vanilla_replay_storage.VanillaReplayStorage]
VanillaRolloutStorage: Type[rllte.xploit.storage.vanilla_rollout_storage.VanillaRolloutStorage]
test_storage: Any

def make_dmc_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., visualize_reward: bool = ..., from_pixels: bool = ..., height: int = ..., width: int = ..., frame_stack: int = ..., action_repeat: int = ...) -> Any: ...
