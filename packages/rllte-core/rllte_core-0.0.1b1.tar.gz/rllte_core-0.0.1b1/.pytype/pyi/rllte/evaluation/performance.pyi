# (generated with --quick)

import numpy as np
import rllte.evaluation.utils
from numpy import random
from scipy import stats as sts
from typing import Any, Callable, Dict, List, Tuple, Type, Union

StratifiedBootstrap: Type[rllte.evaluation.utils.StratifiedBootstrap]

class Performance:
    __doc__: str
    confidence_interval_size: float
    get_ci: bool
    method: str
    random_state: Any
    reps: int
    scores: np.ndarray[Any, np.dtype]
    task_bootstrap: bool
    def __init__(self, scores: np.ndarray, get_ci: bool = ..., method: str = ..., task_bootstrap: bool = ..., reps: int = ..., confidence_interval_size: float = ..., random_state = ...) -> None: ...
    def aggregate_iqm(self) -> Tuple[np.ndarray, Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]]: ...
    def aggregate_mean(self) -> Tuple[np.ndarray, Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]]: ...
    def aggregate_median(self) -> Tuple[np.ndarray, Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]]: ...
    def aggregate_og(self, gamma: float = ...) -> Tuple[np.ndarray, Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]]: ...
    def create_performance_profile(self, tau_list: Union[np.ndarray, List[float]], use_score_distribution: bool = ...) -> Tuple[np.ndarray, Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]]: ...
    def get_interval_estimates(self, scores: np.ndarray, metric: Callable) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]: ...
