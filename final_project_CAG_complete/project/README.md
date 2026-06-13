# CAG Integration Project

Sistema monolítico con integración de Context Augmented Generation (CAG) sobre base RAG existente.

## Description

El asistente combina dos capas de conocimiento:
- **RAG** (Retrieval Augmented Generation): recupera fragmentos relevantes de `data/knowledge_base.json`.
- **CAG** (Context Augmented Generation): enriquece la respuesta con contexto persistente del usuario (preferencias, audiencia, historial).

## Architecture

```
Frontend (index.html / app.js)
         ↓  HTTP JSON
Backend API (server.py)
         ↓
    ┌────┴────┐
    ▼         ▼
CAG Layer   RAG Layer
(cag/)    (knowledge.py)
    ↓         ↓
ContextStore  knowledge_base.json
(data/cag_context.json)
```

### Key modules

| Módulo | Responsabilidad |
|---|---|
| `backend/context_store.py` | Persistencia JSON de contexto por usuario |
| `backend/cag/apply_context.py` | Enriquece la respuesta RAG con contexto CAG |
| `backend/cag/context_manager.py` | Fachada: save_context / retrieve_context / build_context_prompt |
| `backend/assistant.py` | Orquesta RAG + CAG para responder preguntas |
| `backend/server.py` | Servidor HTTP con API REST JSON |

## Installation

```bash
# Python 3.12+ required — no external dependencies for runtime
pip install pytest   # only needed for tests
```

## Running

```bash
PYTHONPATH=. python3 -m backend.server
# Backend at http://127.0.0.1:8000
```

Open `frontend/index.html` in a browser.

## Tests

```bash
# All tests
PYTHONPATH=. python3 -m pytest tests/ -v

# By category
PYTHONPATH=. python3 -m pytest tests/base/        # Base API tests
PYTHONPATH=. python3 -m pytest tests/unit/        # TDD unit tests
PYTHONPATH=. python3 -m pytest tests/bdd/         # BDD scenario tests
PYTHONPATH=. python3 -m pytest tests/validation/  # CAG contract tests
```

Expected: **17 passed**.

## Scrum Process

| Sprint | Objetivo | Commit |
|---|---|---|
| Sprint 1 | Análisis y diseño — fork, ejecución, revisión de arquitectura, backlog, SDD inicial | `Sprint 1 - Project analysis and architecture documentation` |
| Sprint 2 | Desarrollo CAG — ContextStore, ContextManager, persistencia JSON | `Sprint 2 - Implement CAG context persistence` |
| Sprint 3 | BDD + TDD — escenarios Gherkin, pruebas unitarias e integración | `Sprint 3 - Add BDD scenarios and automated tests` |
| Sprint 4 | Integración y documentación — README, evidencias, PR, merge | `Sprint 4 - Final integration and documentation` |

## BDD

Escenarios en `docs/BDD.feature`:

```gherkin
Feature: Context Augmented Generation

  Scenario: Remember user name
    Given a user starts a conversation
    When the user says "My name is Julio"
    And later asks "What is my name?"
    Then the system should answer "Your name is Julio"

  Scenario: Remember preferred technology
    Given a user says "I work with Python"
    When the user later asks "What technology do I use?"
    Then the system should answer "Python"
```

Implementados en `tests/bdd/test_cag_scenarios.py`.

## TDD

Flujo TDD aplicado en `tests/unit/test_context_store.py`:

```python
# 1. Se escribe el test PRIMERO:
def test_context_is_saved(tmp_store):
    tmp_store.save("user1", "name", "Julio")
    context = tmp_store.list_for_user("user1")
    values = [item["value"] for item in context]
    assert "Julio" in values

# 2. Se implementa ContextStore.save() para que pase.
```

7 pruebas TDD cubren: guardado, actualización de clave, aislamiento de usuarios, persistencia entre instancias.

## Evidence

Screenshots y evidencias del proceso en `docs/evidencias/`.

## AI Usage

Ver [docs/PROMPTS.md](docs/PROMPTS.md) — registro cronológico de 5 prompts con objetivo, respuesta IA, decisión humana, cambios realizados y verificación.
