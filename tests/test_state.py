import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parent.parent / "sync"))
import state  # noqa: E402


def _node(source_path, mtime):
    return SimpleNamespace(source_path=source_path, mtime=mtime)


# --- get_changed_nodes --------------------------------------------------

def test_get_changed_nodes_empty_state_returns_all():
    nodes = [_node("/a.md", 1.0), _node("/b.md", 2.0)]
    assert state.get_changed_nodes(nodes, {}) == nodes


def test_get_changed_nodes_only_newer():
    a = _node("/a.md", 100.0)  # newer than recorded
    b = _node("/b.md", 50.0)   # equal to recorded -> not changed
    st = {"/a.md": 90.0, "/b.md": 50.0}
    changed = state.get_changed_nodes([a, b], st)
    assert changed == [a]


def test_get_changed_nodes_unknown_path_is_changed():
    a = _node("/new.md", 0.5)
    assert state.get_changed_nodes([a], {"/old.md": 10.0}) == [a]


# --- mark_synced --------------------------------------------------------

def test_mark_synced_maps_path_to_mtime():
    nodes = [_node(Path("/a.md"), 1.0), _node(Path("/b.md"), 2.0)]
    updated = state.mark_synced(nodes, {})
    assert updated == {"/a.md": 1.0, "/b.md": 2.0}
    # keys are stringified paths
    assert all(isinstance(k, str) for k in updated)


def test_mark_synced_does_not_mutate_input():
    original = {"/existing.md": 5.0}
    nodes = [_node("/a.md", 1.0)]
    updated = state.mark_synced(nodes, original)
    assert original == {"/existing.md": 5.0}  # unchanged
    assert updated == {"/existing.md": 5.0, "/a.md": 1.0}


# --- load_state / save_state round-trip ---------------------------------

def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    state_file = tmp_path / ".sync_state.json"
    monkeypatch.setattr(state, "STATE_FILE", state_file)

    data = {"/x.md": 1.5, "/y.md": 99.0}
    state.save_state(data)
    assert state_file.exists()
    assert state.load_state() == data


def test_load_state_missing_file_returns_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(state, "STATE_FILE", tmp_path / "missing.json")
    assert state.load_state() == {}
