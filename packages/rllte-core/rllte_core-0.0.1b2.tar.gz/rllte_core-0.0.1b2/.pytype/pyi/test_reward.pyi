# (generated with --quick)

import pytest
import rllte.xplore.reward.girm
import rllte.xplore.reward.icm
import rllte.xplore.reward.ngu
import rllte.xplore.reward.pseudo_counts
import rllte.xplore.reward.re3
import rllte.xplore.reward.revd
import rllte.xplore.reward.ride
import rllte.xplore.reward.rise
import rllte.xplore.reward.rnd
import torch as th
from typing import Any, Type

GIRM: Type[rllte.xplore.reward.girm.GIRM]
ICM: Type[rllte.xplore.reward.icm.ICM]
NGU: Type[rllte.xplore.reward.ngu.NGU]
PseudoCounts: Type[rllte.xplore.reward.pseudo_counts.PseudoCounts]
RE3: Type[rllte.xplore.reward.re3.RE3]
REVD: Type[rllte.xplore.reward.revd.REVD]
RIDE: Type[rllte.xplore.reward.ride.RIDE]
RISE: Type[rllte.xplore.reward.rise.RISE]
RND: Type[rllte.xplore.reward.rnd.RND]
test_reward: Any

def make_atari_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., frame_stack: int = ..., distributed: bool = ...) -> Any: ...
def make_dmc_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., visualize_reward: bool = ..., from_pixels: bool = ..., height: int = ..., width: int = ..., frame_stack: int = ..., action_repeat: int = ...) -> Any: ...
