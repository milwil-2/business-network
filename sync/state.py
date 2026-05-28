import json
from pathlib import Path

STATE_FILE = Path(__file__).parent / ".sync_state.json"


def load_state() -> dict[str, float]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict[str, float]):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_changed_nodes(nodes, state: dict) -> list:
    return [n for n in nodes if state.get(str(n.source_path), 0) < n.mtime]


def mark_synced(nodes, state: dict) -> dict:
    updated = dict(state)
    for n in nodes:
        updated[str(n.source_path)] = n.mtime
    return updated
