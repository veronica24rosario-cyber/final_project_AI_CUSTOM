# Software Design Document (SDD)
## CAG Integration — Proyecto Examen Final Módulo 3

---

## 1. Introducción

### 1.1 Purpose
Este documento describe el diseño de la integración del módulo **Context Augmented Generation (CAG)** en el sistema monolítico existente. El objetivo es enriquecer las respuestas del asistente con contexto persistente por usuario, complementando el módulo RAG ya presente.

### 1.2 Scope
El documento cubre:
- Análisis de la arquitectura base.
- Diseño del módulo CAG (ContextStore, ContextManager, apply_context).
- Capa de persistencia JSON.
- Integración con el servidor HTTP y el asistente.
- Estrategia de pruebas (TDD + BDD).

### 1.3 Definitions
| Término | Definición |
|---|---|
| RAG | Retrieval Augmented Generation — recupera fragmentos de base documental. |
| CAG | Context Augmented Generation — usa contexto persistente del usuario. |
| ContextStore | Componente responsable de guardar y recuperar contexto por usuario. |
| ContextManager | Fachada de alto nivel sobre ContextStore con lógica de prompt-building. |
| user_id | Identificador único del usuario a través de todas las sesiones. |

---

## 2. Arquitectura

### 2.1 Vista de componentes

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
(JSON file)
```

### 2.2 Flujo de una pregunta

1. El frontend envía `POST /api/ask` con `user_id` y `question`.
2. `server.py` delega a `answer_question(user_id, question, context_store)`.
3. **RAG**: `retrieve_snippets(question)` busca en `knowledge_base.json`.
4. Se construye `base_answer` con los fragmentos recuperados.
5. **CAG**: `context_store.list_for_user(user_id)` devuelve el contexto guardado.
6. `apply_context(...)` enriquece `base_answer` con el contexto.
7. Se devuelve `{answer, sources, context_used}` al cliente.

---

## 3. Diseño del módulo CAG

### 3.1 ContextStore

**Responsabilidad**: Persistir pares clave-valor de contexto por usuario en un archivo JSON.

| Interfaz | Descripción |
|---|---|
| `save(user_id, key, value) → bool` | Guarda o actualiza una entrada de contexto. |
| `list_for_user(user_id) → list[dict]` | Recupera todas las entradas para un usuario. |

**Entradas**: `user_id: str`, `key: str`, `value: Any`  
**Salidas**: `stored_context: list[{"key": str, "value": Any}]`  
**Almacenamiento**: `data/cag_context.json`

### 3.2 ContextManager

**Responsabilidad**: Fachada de alto nivel con las tres operaciones canónicas del CAG.

| Método | Descripción |
|---|---|
| `save_context(user_id, message)` | Persiste un mensaje como entrada de contexto. |
| `retrieve_context(user_id)` | Devuelve todos los items de contexto del usuario. |
| `build_context_prompt(user_id)` | Construye un bloque de texto para el prompt del LLM. |

### 3.3 apply_context

**Responsabilidad**: Recibe la respuesta RAG base y la enriquece con los items de contexto del usuario.

**Firma**:
```python
apply_context(user_id, question, base_answer, context_items) → (str, list[str])
```

Devuelve `(augmented_answer, used_keys)`.

---

## 4. Capa de Persistencia

- **Formato**: JSON plano (`data/cag_context.json`).
- **Estructura**:
```json
{
  "user_id_1": [
    {"key": "audience", "value": "principiante"},
    {"key": "project",  "value": "monolito moderno"}
  ]
}
```
- **Estrategia de escritura**: write-through (cada `save` persiste a disco inmediatamente).
- **Evolución futura**: Reemplazable por SQLite o Redis sin cambiar la interfaz pública.

---

## 5. Decisiones de diseño

| Decisión | Razón |
|---|---|
| JSON como almacenamiento inicial | Simplicidad para el prototipo; sin dependencias externas. |
| ContextStore separado de ContextManager | SRP: Storage vs. lógica de negocio. |
| apply_context devuelve `(answer, keys)` | El servidor necesita reportar `context_used` en la respuesta API. |
| context_store compartido en server.py | Estado en memoria + disco coherente para todas las peticiones. |
