"""
ContextManager: high-level facade over ContextStore + CAG augmentation.

Provides the three canonical CAG operations described in the project spec:
  - save_context(user_id, message)
  - retrieve_context(user_id)
  - build_context_prompt(user_id)
"""

from typing import Any

from backend.context_store import ContextStore


class ContextManager:
    """Facade that combines storage and prompt-building for the CAG layer."""

    def __init__(self, store: ContextStore | None = None) -> None:
        self._store = store or ContextStore()

    def save_context(self, user_id: str, message: str) -> bool:
        """
        Parse *message* for a key=value pattern and persist it.

        Simple heuristic: treats the whole message as the value under the
        key "message_<n>" where n is the current item count for the user.

        Args:
            user_id: Unique user identifier.
            message: Free-text message to persist.

        Returns:
            True when saved successfully.
        """
        key = f"message_{len(self._store.list_for_user(user_id))}"
        return self._store.save(user_id, key, message)

    def retrieve_context(self, user_id: str) -> list[dict[str, Any]]:
        """
        Return all context items stored for *user_id*.

        Args:
            user_id: Unique user identifier.

        Returns:
            List of {"key": ..., "value": ...} dicts.
        """
        return self._store.list_for_user(user_id)

    def build_context_prompt(self, user_id: str) -> str:
        """
        Build a plain-text prompt snippet from the user's stored context.

        Intended to be prepended to the final LLM prompt alongside the RAG
        context so the model can personalise its response.

        Args:
            user_id: Unique user identifier.

        Returns:
            A formatted string, or an empty string if no context exists.
        """
        items = self.retrieve_context(user_id)
        if not items:
            return ""
        lines = [f"- {item['key']}: {item['value']}" for item in items]
        return "Contexto del usuario:\n" + "\n".join(lines)
