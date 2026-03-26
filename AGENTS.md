# AGENTS.md

## Proposito
Macro Pulse Chile es un observatorio macroeconomico local-first para comparar Chile con referentes internacionales usando fuentes oficiales y gratuitas. El MVP debe descargar, normalizar, comparar, visualizar y exportar un set cerrado de series sin ampliar el scope.

## Stack y restricciones
- Python 3.11+, Streamlit, Pandas, Plotly, DuckDB, Pydantic, Requests y python-dotenv.
- Calidad y testing: pytest, Ruff y Black.
- Local-first, sin hosting pagado, sin login, sin frontend separado y sin microservicios.
- Fuentes del nucleo MVP: World Bank y FRED. BCCh solo si no bloquea el avance.
- API oficial primero. Selenium solo opcional, publico y nunca como columna vertebral.

## Estructura del repo
- `main.py`: entrypoint Streamlit y navegacion del MVP.
- `app/ui/`: vistas y cache de UI; solo presentacion.
- `src/connectors/`: integraciones externas.
- `src/domain/`: modelos y enums.
- `src/services/`: orquestacion y casos de uso.
- `src/storage/`: persistencia local.
- `src/transform/`: normalizacion, reshape y enriquecimiento.
- `src/config/`: catalogo y configuracion.
- `data/`: datos locales no versionados.
- `tests/`: tests automatizados y fixtures.

## Reglas de cambio
- Lee primero `docs/PROJECT_CONTEXT.md`, `GEMINI.md`, `README.md` y el arbol real.
- Haz cambios pequenos, trazables y auditables; no amplias el scope del MVP.
- No metas logica de negocio, normalizacion, comparacion ni metricas en `app/ui/`.
- Si cambias catalogo, ids, contratos o fuentes, actualiza tests y documentacion en el mismo cambio.
- Si una fuente tiene friccion, crea primero interfaz, stub o fixture; no bloquees el repo por esa fuente.
- Toda salida visible debe mostrar fuente y fecha de actualizacion.
- Toda decision estructural relevante debe quedar en `docs/adr-xxxx.md`.

## Reglas de testing
- Los tests nuevos van en `tests/`; no agregues mas `test_*.py` en la raiz.
- Prioriza fixtures o muestras guardadas; evita depender de red en el flujo normal de pytest.
- Cubre conectores, storage y servicios, incluyendo credenciales ausentes, timeouts, respuestas vacias y persistencia local.
- Si una prueba requiere credenciales reales, dejala como manual y documentala.

## Reglas de documentacion
- `docs/PROJECT_CONTEXT.md` es la fuente canonica de alcance.
- `README.md` solo debe prometer lo que ya existe en el codigo.
- Mantén `.env.example` sin secretos reales.
- Si cambia arquitectura, contratos o estrategia de fuentes, actualiza docs y ADR en el mismo cambio.

## Nunca hacer
- No agregar nuevas pantallas, fuentes o features fuera del MVP cerrado.
- No introducir React/FastAPI, cloud, login, microservicios, tiempo real de mercado o forecasting avanzado.
- No usar Selenium como base del proyecto ni desplazar una API oficial existente.
- No versionar secretos, bases DuckDB, rutas absolutas locales ni artefactos generados.
- No mezclar capas por conveniencia.

## Definicion de terminado para una tarea pequena
- Cambio acotado a una sola preocupacion.
- Capas respetadas.
- Verificacion automatizada o manual documentada.
- Documentacion y catalogo sincronizados si hubo cambios visibles.
- Sin secretos, sin artefactos locales y sin regresiones obvias del flujo local.
