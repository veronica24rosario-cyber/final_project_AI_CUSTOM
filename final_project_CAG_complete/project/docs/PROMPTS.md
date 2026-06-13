# PROMPTS.md — Registro de uso de IA

Documento cronológico de cada interacción significativa con IA durante el desarrollo del módulo CAG.

---

## Prompt 1

**Fecha:** 2026-06-12

**Objetivo:** Analizar la arquitectura del repositorio base y planificar la integración del módulo CAG.

**Prompt:**
```
Actúa como Senior Software Architect. Analiza el repositorio monolítico existente.
Objetivo: Integrar un módulo Context Augmented Generation (CAG) manteniendo la arquitectura existente.
Necesito: análisis de arquitectura, diseño de integración CAG, SDD, backlog Scrum 4 sprints,
escenarios BDD, estrategia TDD, implementación Python Clean Architecture.
```

**Respuesta IA:**
Se identificó que el proyecto tiene `ContextStore` y `cag.py` como stubs con `NotImplementedError`. La arquitectura propuesta fue: `ContextStore` (persistencia JSON) → `apply_context` (enriquecimiento) → integración en `assistant.py`. El servidor ya expone `/api/context` y `/api/ask`; solo falta conectar la lógica.

**Decisión humana:**
Se aceptó la propuesta. Se decidió mantener `backend/cag/` como sub-paquete para Clean Architecture.

**Cambios realizados:**
- Creado `backend/cag/__init__.py`, `apply_context.py`, `context_manager.py`.
- Reemplazados los stubs por implementaciones reales.

**Verificación:**
`PYTHONPATH=. python3 -m pytest tests/ -v` → 6/6 tests de validación contract pasando.

---

## Prompt 2

**Fecha:** 2026-06-12

**Objetivo:** Implementar `ContextStore` con persistencia JSON y typing completo.

**Prompt:**
```
Implementa ContextStore en backend/context_store.py.
Requisitos: guardar key-value por user_id en JSON, actualizar clave existente sin duplicar,
aislar datos entre usuarios, persistir al disco en cada save.
Añade typing completo y docstrings.
```

**Respuesta IA:**
Implementación con `_load()` / `_persist()` privados, `save()` con upsert y `list_for_user()`. Uso de `Path` para rutas cross-platform.

**Decisión humana:**
Se aceptó. Se añadió fixture `tmp_path` en las pruebas para aislar archivos entre tests.

**Cambios realizados:**
- `backend/context_store.py` completamente implementado.
- `tests/unit/test_context_store.py` con 7 pruebas TDD.

**Verificación:**
`pytest tests/unit/` → 7/7 PASSED.

---

## Prompt 3

**Fecha:** 2026-06-12

**Objetivo:** Integrar CAG en `assistant.py` y conectar el `context_store` compartido del servidor.

**Prompt:**
```
Modifica assistant.py para que answer_question reciba un context_store opcional.
Debe: 1) llamar retrieve_snippets (RAG), 2) llamar list_for_user (CAG),
3) llamar apply_context, 4) devolver context_used en la respuesta.
Asegúrate de que server.py pase el context_store compartido.
```

**Respuesta IA:**
Se propuso añadir `context_store: ContextStore | None = None` como parámetro con fallback a instancia global. `server.py` pasa `context_store` explícitamente para compartir estado.

**Decisión humana:**
Se aceptó. La instancia global en `assistant.py` sirve como fallback para tests directos.

**Cambios realizados:**
- `backend/assistant.py` reescrito con integración CAG.
- `backend/server.py` actualizado para pasar `context_store` a `answer_question`.

**Verificación:**
`pytest tests/validation/` → 3/3 PASSED (incluyendo `test_ask_uses_context_to_influence_later_response`).

---

## Prompt 4

**Fecha:** 2026-06-12

**Objetivo:** Crear escenarios BDD y pruebas TDD adicionales.

**Prompt:**
```
Crea tests/bdd/test_cag_scenarios.py con los escenarios Gherkin del enunciado:
- Scenario: Remember user name
- Scenario: Remember preferred technology
Usa ContextManager como sujeto bajo prueba. Añade docstrings con el escenario Gherkin.
```

**Respuesta IA:**
Se generaron clases `TestRememberUserName` y `TestRememberPreferredTechnology` con fixtures `tmp_path` y `ContextManager`.

**Decisión humana:**
Se aceptó. Se verificó que los escenarios cubren los criterios de aceptación del enunciado.

**Cambios realizados:**
- `tests/bdd/test_cag_scenarios.py` creado con 4 pruebas BDD.

**Verificación:**
`pytest tests/bdd/` → 4/4 PASSED.

---

## Prompt 5

**Fecha:** 2026-06-12

**Objetivo:** Generar documentación final (SDD, README, PROMPTS.md).

**Prompt:**
```
Genera el SDD con secciones: Purpose, Scope, Definitions, Arquitectura, diseño CAG,
persistencia, decisiones de diseño. Genera README con descripción, arquitectura,
instalación, ejecución, tests, proceso Scrum, BDD, TDD, evidencias, uso de IA.
```

**Respuesta IA:**
Generados todos los documentos con diagramas ASCII, tablas de interfaces y secciones requeridas.

**Decisión humana:**
Se aceptó. Se revisó que el README incluya todos los apartados del rúbrica.

**Cambios realizados:**
- `docs/SDD.md`, `docs/PROMPTS.md`, `README.md` creados/actualizados.

**Verificación:**
Suite completa: `pytest tests/ -v` → 17/17 PASSED.
