import importlib
import pkgutil
from pathlib import Path

from google.adk.agents import BaseAgent

_ROOT = Path(__file__).parent


def _discover_sub_agents() -> list[BaseAgent]:
    base = _ROOT / "sub_agents"
    found = []
    for _, name, is_pkg in sorted(pkgutil.iter_modules([str(base)])):
        if not is_pkg:
            continue
        module_path = f"agents.root_agent.sub_agents.{name}.agent"
        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            print(f"[registry] ❌ {module_path} import 실패: {e}")
            continue
        candidate = getattr(module, name, None)
        if isinstance(candidate, BaseAgent):
            found.append(candidate)
        else:
            print(
                f"[registry] ⚠️ {module_path}에 '{name}' 이름의 BaseAgent 변수가 없습니다. "
                f"(현재 모듈에 있는 이름들: {[n for n in dir(module) if not n.startswith('_')]})"
            )
    return found


def _discover_pipelines() -> list[BaseAgent]:
    base = _ROOT / "pipelines"
    found = []
    for _, name, is_pkg in sorted(pkgutil.iter_modules([str(base)])):
        if is_pkg:
            continue
        module_path = f"agents.root_agent.pipelines.{name}"
        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            print(f"[registry] ❌ {module_path} import 실패: {e}")
            continue
        candidate = getattr(module, name, None)
        if isinstance(candidate, BaseAgent):
            found.append(candidate)
        else:
            print(
                f"[registry] ⚠️ {module_path}.py 파일 안에 '{name}' 이름의 "
                f"SequentialAgent 변수가 없습니다. "
                f"(현재 모듈에 있는 이름들: {[n for n in dir(module) if not n.startswith('_')]})"
            )
    return found


def discover_all_agents() -> list[BaseAgent]:
    agents = _discover_sub_agents() + _discover_pipelines()
    print(f"[registry] 총 {len(agents)}개 에이전트 로드 완료: {[a.name for a in agents]}")
    return agents
