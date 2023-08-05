# (generated with --quick)

import rllte.common.base_augmentation
import torch as th
from torch.nn import functional as F
from typing import Any, Type

BaseAugmentation: Type[rllte.common.base_augmentation.BaseAugmentation]

class RandomCrop(rllte.common.base_augmentation.BaseAugmentation):
    __doc__: str
    _out: int
    _pad: int
    def __init__(self, pad: int = ..., out: int = ...) -> None: ...
    def forward(self, x) -> Any: ...
