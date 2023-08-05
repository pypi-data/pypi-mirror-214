# (generated with --quick)

import argparse
import os
import rllte.xploit.agent.drqv2
from typing import Any, Type

DrQv2: Type[rllte.xploit.agent.drqv2.DrQv2]
agent: rllte.xploit.agent.drqv2.DrQv2
args: argparse.Namespace
env: Any
eval_env: Any
parser: argparse.ArgumentParser

def make_dmc_env(env_id: str = ..., num_envs: int = ..., device: str = ..., seed: int = ..., visualize_reward: bool = ..., from_pixels: bool = ..., height: int = ..., width: int = ..., frame_stack: int = ..., action_repeat: int = ...) -> Any: ...
