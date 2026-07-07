# test/check_registry.py
from agents.root_agent.registry import discover_all_agents

for a in discover_all_agents():
    print(f"- {a.name}: {a.description}")