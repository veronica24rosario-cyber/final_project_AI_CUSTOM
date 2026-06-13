"""
ContextStore: Persistent key-value context storage per user.

Responsibilities:
- Persist user context items (key/value pairs) across requests.
- Provide retrieval of all context items for a given user.

Storage backend: JSON file (data/cag_context.json).
"""

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTEXT_FILE = PROJECT_ROOT / "data" / "cag_context.json"


class ContextStore:
    """Stores and retrieves per-user context items backed by a JSON file."""

    def __init__(self, path: Path = CONTEXT_FILE) -> None:
        self._path = path
        self._data: dict[str, list[dict[str, Any]]] = self._load()

    # ------------------------------------------------------------------ #
    # Private helpers                                                      #
    # ------------------------------------------------------------------ #

    def _load(self) -> dict[str, list[dict[str, Any]]]:
        """Load existing context from disk, or return empty dict."""
        if self._path.exists():
            with open(self._path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _persist(self) -> None:
        """Write current in-memory state to disk."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def save(self, user_id: str, key: str, value: Any) -> bool:
        """
        Save or update a context item for a user.

        Args:
            user_id: Unique identifier for the user.
            key:     Context key (e.g. "preferred_style", "audience").
            value:   Value to associate with that key.

        Returns:
            True when the item was persisted successfully.
        """
        if user_id not in self._data:
            self._data[user_id] = []

        # Update existing key if present, otherwise append.
        for item in self._data[user_id]:
            if item["key"] == key:
                item["value"] = value
                self._persist()
                return True

        self._data[user_id].append({"key": key, "value": value})
        self._persist()
        return True

    def list_for_user(self, user_id: str) -> list[dict[str, Any]]:
        """
        Retrieve all context items stored for a user.

        Args:
            user_id: Unique identifier for the user.

        Returns:
            List of {"key": ..., "value": ...} dicts (may be empty).
        """
        return list(self._data.get(user_id, []))
