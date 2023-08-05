# (generated with --quick)

import rllte.common.base_augmentation
import torch as th
from typing import Any, Type

BaseAugmentation: Type[rllte.common.base_augmentation.BaseAugmentation]

class RandomRotate(rllte.common.base_augmentation.BaseAugmentation):
    __doc__: str
    p: float
    def __init__(self, p: float = ...) -> None: ...
    def forward(self, x) -> Any: ...
