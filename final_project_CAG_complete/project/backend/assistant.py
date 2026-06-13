"""
Assistant: orchestrates RAG + CAG to answer user questions.

Flow:
  1. Retrieve snippets from the knowledge base (RAG).
  2. Build a base answer from those snippets.
  3. Load the user's persisted context (CAG).
  4. Augment the base answer with the context (CAG).
  5. Return the final answer with metadata.
"""

from backend.cag import apply_context
from backend.context_store import ContextStore
from backend.knowledge import retrieve_snippets

# Shared store instance used by the assistant (server injects its own too).
_store = ContextStore()


def answer_question(
    user_id: str,
    question: str,
    context_store: ContextStore | None = None,
) -> dict:
    """
    Answer *question* for *user_id* using RAG + CAG.

    Args:
        user_id:       Unique identifier for the user.
        question:      The question text.
        context_store: Optional ContextStore override (useful for testing).

    Returns:
        Dict with keys: user_id, answer, sources, context_used.
    """
    store = context_store or _store

    # ── RAG layer ──────────────────────────────────────────────────────────
    snippets = retrieve_snippets(question)

    if snippets:
        source_text = " ".join(item["content"] for item in snippets)
        base_answer = f"Segun la base de conocimiento del curso: {source_text}"
        sources = [item["id"] for item in snippets]
    else:
        base_answer = "No encontre informacion suficiente en la base de conocimiento del curso."
        sources = []

    # ── CAG layer ──────────────────────────────────────────────────────────
    context_items = store.list_for_user(user_id)
    final_answer, context_used = apply_context(
        user_id, question, base_answer, context_items
    )

    return {
        "user_id": user_id,
        "answer": final_answer,
        "sources": sources,
        "context_used": context_used,
    }
