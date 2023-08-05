# (generated with --quick)

import io
import numpy as np
import pathlib
import random
from typing import Dict, Type

Path: Type[pathlib.Path]

def episode_len(episode: Dict[str, np.ndarray]) -> int: ...
def load_episode(fn: pathlib.Path) -> Dict[str, np.ndarray]: ...
def save_episode(episode: Dict[str, np.ndarray], fn: pathlib.Path) -> None: ...
def worker_init_fn(worker_id: int) -> None: ...
