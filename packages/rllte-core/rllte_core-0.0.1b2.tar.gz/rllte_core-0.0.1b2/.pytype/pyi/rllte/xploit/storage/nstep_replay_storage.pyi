# (generated with --quick)

import collections
import datetime
import gymnasium as gym
import numpy as np
import pathlib
import random
import rllte.common.base_storage
import torch as th
import traceback
from typing import Annotated, Any, Dict, Iterator, List, Type

BaseStorage: Type[rllte.common.base_storage.BaseStorage]
IterableDataset: Any
Path: Type[pathlib.Path]
defaultdict: Type[collections.defaultdict]

class NStepReplayStorage(rllte.common.base_storage.BaseStorage):
    __doc__: str
    _replay_iter: Any
    replay_dir: pathlib.Path
    replay_iter: Annotated[Iterator, 'property']
    replay_loader: Any
    replay_storage: ReplayStorage
    def __init__(self, observation_space, action_space, device: str = ..., storage_size: int = ..., batch_size: int = ..., num_workers: int = ..., pin_memory: bool = ..., n_step: int = ..., discount: float = ..., fetch_every: int = ..., save_snapshot: bool = ...) -> None: ...
    def add(self, obs: np.ndarray, action: np.ndarray, reward: np.ndarray, terminated: np.ndarray, truncated: np.ndarray, info: Dict[str, Any], next_obs: np.ndarray) -> None: ...
    def sample(self, step: int) -> tuple: ...
    def update(self, *args) -> None: ...

class ReplayStorage:
    __doc__: str
    _current_episode: collections.defaultdict[str, Any]
    _num_episodes: int
    _num_transitions: int
    _replay_dir: pathlib.Path
    def __init__(self, replay_dir: pathlib.Path) -> None: ...
    def __len__(self) -> int: ...
    def _preload(self) -> None: ...
    def _store_episode(self, episode: Dict[str, np.ndarray]) -> None: ...
    def add(self, obs: np.ndarray, action: np.ndarray, reward: np.ndarray, terminated: np.ndarray, truncated: np.ndarray, info: Dict[str, Any], next_obs: np.ndarray) -> None: ...

class ReplayStorageDataset(Any):
    __doc__: str
    _discount: float
    _episode_fns: List[pathlib.Path]
    _episodes: Dict[pathlib.Path, Dict[str, np.ndarray[Any, np.dtype]]]
    _fetch_every: int
    _max_size: int
    _nstep: int
    _num_workers: int
    _replay_dir: pathlib.Path
    _samples_since_last_fetch: int
    _save_snapshot: bool
    _size: int
    def __init__(self, replay_dir: pathlib.Path, max_size: int, num_workers: int, nstep: int, discount: float, fetch_every: int, save_snapshot: bool) -> None: ...
    def __iter__(self) -> Iterator: ...
    def _sample(self) -> tuple: ...
    def _sample_episode(self) -> Dict[str, np.ndarray]: ...
    def _store_episode(self, eps_fn: pathlib.Path) -> bool: ...
    def _try_fetch(self) -> None: ...

def episode_len(episode: Dict[str, np.ndarray]) -> int: ...
def load_episode(fn: pathlib.Path) -> Dict[str, np.ndarray]: ...
def save_episode(episode: Dict[str, np.ndarray], fn: pathlib.Path) -> None: ...
def worker_init_fn(worker_id: int) -> None: ...
