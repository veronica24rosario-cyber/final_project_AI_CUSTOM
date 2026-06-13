"""
apply_context: augment a base answer with user context items.
"""
from typing import Any


def apply_context(
    user_id: str,
    question: str,
    base_answer: str,
    context_items: list[dict[str, Any]],
) -> tuple[str, list[str]]:
    if not context_items:
        return base_answer, []

    used_keys: list[str] = []
    notes: list[str] = []

    for item in context_items:
        key: str = item["key"]
        value: Any = item["value"]
        notes.append(f"(Contexto personal — {key}: {value})")
        used_keys.append(key)

    augmented = base_answer + " " + " ".join(notes)
    return augmented, used_keys
