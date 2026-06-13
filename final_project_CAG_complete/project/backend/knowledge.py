import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "data" / "knowledge_base.json"


def load_knowledge_base(path=KNOWLEDGE_BASE_PATH):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_snippets(question, knowledge_base=None, limit=2):
    knowledge_base = knowledge_base or load_knowledge_base()
    terms = set(question.lower().replace("?", "").replace(",", "").split())
    scored = []

    for item in knowledge_base:
        haystack = f"{item['title']} {item['content']}".lower()
        score = sum(1 for term in terms if term in haystack)
        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored[:limit]]
