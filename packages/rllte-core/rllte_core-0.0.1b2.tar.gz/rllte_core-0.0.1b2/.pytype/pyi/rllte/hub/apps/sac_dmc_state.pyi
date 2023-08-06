# (generated with --quick)

import argparse
import os
import rllte.xploit.agent.sac
from typing import Any, Type

SAC: Type[rllte.xploit.agent.sac.SAC]
agent: rllte.xploit.agent.sac.SAC
args: argparse.Namespace
env: Any
eval_env: Any
parser: argparse.ArgumentParser

def make_dmc_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., visualize_reward: bool = ..., from_pixels: bool = ..., height: int = ..., width: int = ..., frame_stack: int = ..., action_repeat: int = ...) -> Any: ...
