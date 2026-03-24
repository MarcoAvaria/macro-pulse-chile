# GEMINI.md

## Rol esperado
Actúa como colaborador técnico del proyecto **Macro Pulse Chile**.

Tu prioridad es ayudar a construir un MVP **local-first**, modular y controlado, evitando scope creep y decisiones que metan complejidad prematura.

## Documento fuente principal
Lee primero `PROJECT_CONTEXT.md`.

Ese archivo es la referencia canónica del proyecto. No lo contradigas sin justificarlo.

## Cómo trabajar en este repositorio

1. Revisa primero la estructura del proyecto.
2. Revisa `PROJECT_CONTEXT.md` antes de proponer cambios grandes.
3. Propón cambios pequeños, trazables y revisables.
4. Separa claramente capas de conectores, transformación, servicios y UI.
5. No metas lógica de negocio en la UI.
6. Si una API es difícil de conectar, crea primero interfaz + stub + fixture.
7. No bloquees el avance general por una fuente secundaria.
8. Prioriza entregables funcionales antes que refinamientos estéticos.

## Objetivo actual del proyecto
Construir un observatorio macroeconómico local que permita:
- descargar series públicas oficiales,
- normalizarlas,
- compararlas,
- visualizarlas,
- y exportar reportes.

## Prioridades técnicas actuales

### Fase 1
- estructura base del repositorio,
- configuración del proyecto,
- catálogo inicial de series,
- conector World Bank,
- conector FRED,
- normalización de series,
- persistencia local.

### Fase 2
- vistas de Series, Comparar y Reporte,
- exportación,
- pruebas mínimas,
- fixtures.

### Fase 3
- evaluar BCCh,
- ajustes de UX,
- mejoras de performance,
- mejoras de reporte.

## Qué no debes empujar de entrada
- frontend separado React/FastAPI,
- hosting cloud,
- login de usuarios,
- microservicios,
- tiempo real de mercado,
- forecasting complejo,
- scraping innecesario,
- Selenium como dependencia principal.

## Regla sobre Selenium
Selenium solo puede entrar como módulo opcional si:
- la fuente es pública,
- no hay API oficial equivalente,
- no hay login,
- no hay restricciones dudosas,
- y su uso no deforma el MVP.

## Estilo de trabajo esperado
- Prefiere claridad sobre brillo.
- Prefiere estructura sobre velocidad desordenada.
- Prefiere MVP cerrado sobre ambición difusa.
- Si detectas scope creep, dilo explícitamente.
- Si una sugerencia contradice el contexto del proyecto, explica por qué.

## Formato preferido para propuestas
Cuando propongas cambios importantes, responde idealmente con esta estructura:
- diagnóstico,
- causa raíz,
- impacto,
- alternativas,
- recomendación final,
- siguiente paso.

## Convenciones mínimas
- Toda serie debe tener fuente y metadata clara.
- Toda salida visible debe indicar fecha de actualización y fuente.
- Toda integración externa debe tener al menos un fixture o muestra guardada.
- Toda decisión estructural relevante debe quedar registrada en `docs/adr-xxxx.md`.

## Regla de cierre
No intentes convertir Macro Pulse Chile en una plataforma gigante.
Primero construye una base local, seria, explicable y demostrable.
