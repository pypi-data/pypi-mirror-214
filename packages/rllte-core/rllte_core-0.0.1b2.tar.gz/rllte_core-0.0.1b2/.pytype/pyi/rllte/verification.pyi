# (generated with --quick)

import rllte.xploit.agent.ppo
from typing import Any, Callable, Dict, Iterable, Optional, Type, Union

PPO: Type[rllte.xploit.agent.ppo.PPO]
agent: rllte.xploit.agent.ppo.PPO
env: Any

def colored(text: str, color: Optional[str] = ..., on_color: Optional[str] = ..., attrs: Optional[Iterable[str]] = ...) -> str: ...
def make_rllte_env(env_id: Union[str, Callable], num_envs: int = ..., seed: int = ..., device: str = ..., parallel: bool = ..., env_kwargs: Optional[Dict[str, Any]] = ...) -> Any: ...
