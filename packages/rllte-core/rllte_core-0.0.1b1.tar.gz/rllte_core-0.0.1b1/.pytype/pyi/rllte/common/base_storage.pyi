# (generated with --quick)

import abc
import gymnasium as gym
import torch as th
from typing import Any, Callable, List, Type, TypeVar, Union

ABC: Type[abc.ABC]

_FuncT = TypeVar('_FuncT', bound=Callable)

class BaseStorage(abc.ABC):
    __doc__: str
    action_dim: Any
    action_range: List[Union[float, int]]
    action_shape: Any
    action_type: str
    device: Any
    obs_shape: Any
    def __init__(self, observation_space, action_space, device: str = ...) -> None: ...
    @abstractmethod
    def add(self, *args) -> None: ...
    @abstractmethod
    def sample(self, *args) -> Any: ...
    @abstractmethod
    def update(self, *args) -> None: ...

def abstractmethod(funcobj: _FuncT) -> _FuncT: ...
