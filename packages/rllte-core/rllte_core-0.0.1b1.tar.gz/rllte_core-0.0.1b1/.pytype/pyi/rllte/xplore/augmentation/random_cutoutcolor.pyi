# (generated with --quick)

import rllte.common.base_augmentation
import torch as th
from typing import Any, Type

BaseAugmentation: Type[rllte.common.base_augmentation.BaseAugmentation]

class RandomCutoutColor(rllte.common.base_augmentation.BaseAugmentation):
    __doc__: str
    max_cut: int
    min_cut: int
    def __init__(self, min_cut: int = ..., max_cut: int = ...) -> None: ...
    def forward(self, x) -> Any: ...
