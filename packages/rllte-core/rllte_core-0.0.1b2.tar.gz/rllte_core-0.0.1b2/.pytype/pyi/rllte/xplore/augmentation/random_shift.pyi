# (generated with --quick)

import rllte.common.base_augmentation
import torch as th
from torch.nn import functional as F
from typing import Any, Type

BaseAugmentation: Type[rllte.common.base_augmentation.BaseAugmentation]

class RandomShift(rllte.common.base_augmentation.BaseAugmentation):
    __doc__: str
    pad: int
    def __init__(self, pad: int = ...) -> None: ...
    def forward(self, x) -> Any: ...
