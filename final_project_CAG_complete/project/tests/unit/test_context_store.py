"""TDD unit tests for ContextStore."""
import tempfile
from pathlib import Path

import pytest

from backend.context_store import ContextStore


@pytest.fixture
def tmp_store(tmp_path):
    """ContextStore backed by a temporary JSON file."""
    return ContextStore(path=tmp_path / "ctx.json")


def test_context_is_saved(tmp_store):
    tmp_store.save("user1", "name", "Julio")
    context = tmp_store.list_for_user("user1")
    values = [item["value"] for item in context]
    assert "Julio" in values


def test_save_returns_true(tmp_store):
    result = tmp_store.save("user1", "lang", "Python")
    assert result is True


def test_list_empty_for_unknown_user(tmp_store):
    assert tmp_store.list_for_user("ghost") == []


def test_multiple_keys_stored(tmp_store):
    tmp_store.save("u1", "name", "Ana")
    tmp_store.save("u1", "tech", "Python")
    items = tmp_store.list_for_user("u1")
    keys = [i["key"] for i in items]
    assert "name" in keys
    assert "tech" in keys


def test_update_existing_key(tmp_store):
    tmp_store.save("u1", "lang", "Java")
    tmp_store.save("u1", "lang", "Python")
    items = tmp_store.list_for_user("u1")
    lang_values = [i["value"] for i in items if i["key"] == "lang"]
    assert lang_values == ["Python"]
    assert len(lang_values) == 1


def test_isolated_users(tmp_store):
    tmp_store.save("alice", "name", "Alice")
    tmp_store.save("bob", "name", "Bob")
    assert tmp_store.list_for_user("alice")[0]["value"] == "Alice"
    assert tmp_store.list_for_user("bob")[0]["value"] == "Bob"


def test_persistence_across_instances(tmp_path):
    path = tmp_path / "ctx.json"
    store1 = ContextStore(path=path)
    store1.save("u", "k", "v")

    store2 = ContextStore(path=path)
    assert store2.list_for_user("u")[0]["value"] == "v"
