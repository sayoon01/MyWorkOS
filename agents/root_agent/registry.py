import importlib
import pkgutil
from pathlib import Path

from google.adk.agents import BaseAgent

_ROOT = Path(__file__).parent


def _discover_sub_agents() -> list[BaseAgent]:
    """sub_agents/<name>/agent.py 안의 <name> 변수를 자동으로 수집."""
    base = _ROOT / "sub_agents"
    found = []
    for _, name, is_pkg in sorted(pkgutil.iter_modules([str(base)])):
        if not is_pkg:
            continue
        module = importlib.import_module(f"agents.root_agent.sub_agents.{name}.agent")
        candidate = getattr(module, name, None)
        if isinstance(candidate, BaseAgent):
            found.append(candidate)
    return found


def _discover_pipelines() -> list[BaseAgent]:
    """pipelines/<name>_pipeline.py 안의 동일한 이름 변수를 자동으로 수집."""
    base = _ROOT / "pipelines"
    found = []
    for _, name, is_pkg in sorted(pkgutil.iter_modules([str(base)])):
        if is_pkg:
            continue
        module = importlib.import_module(f"agents.root_agent.pipelines.{name}")
        candidate = getattr(module, name, None)
        if isinstance(candidate, BaseAgent):
            found.append(candidate)
    return found


def discover_all_agents() -> list[BaseAgent]:
    return _discover_sub_agents() + _discover_pipelines()
