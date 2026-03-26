# Macro Pulse Chile — Project Context

## 1) Qué es este proyecto

**Macro Pulse Chile** es un observatorio macroeconómico **local-first** orientado a comparar a Chile contra pares y referencias internacionales usando **fuentes oficiales y gratuitas**.

El objetivo es construir una aplicación técnica, seria y presentable, que permita:
- ingerir series públicas macroeconómicas y financieras,
- normalizarlas,
- compararlas,
- visualizarlas,
- y exportar resúmenes y reportes reproducibles.

## 2) Qué no es este proyecto

No es:
- un terminal financiero tipo trading,
- una plataforma multiusuario en esta fase,
- un proyecto dependiente de hosting pagado,
- un producto centrado en tiempo real bursátil,
- un proyecto que dependa de Selenium como columna vertebral,
- un proyecto de machine learning o forecasting avanzado en el MVP.

## 3) Restricciones reales del proyecto

Estas restricciones son estructurales y deben respetarse:
- **Cero hosting pagado** en la fase inicial.
- El proyecto debe poder **correr localmente**.
- Debe poder **probarse con recursos propios**.
- Debe depender de **APIs públicas, gratuitas y/o datasets oficiales reutilizables**.
- Debe evitar depender de accesos privados, empresas, credenciales complejas o infraestructura ajena no controlada.
- Debe tener un **MVP cerrado** para no repetir el crecimiento desbordado de otros proyectos.

## 4) Pregunta guía del producto

- ¿Cómo se está moviendo Chile en inflación, actividad, tasas, tipo de cambio y variables afines frente a sus propios históricos y frente a referentes externos?
- ¿Qué series vale la pena vigilar juntas porque cuentan una historia más útil que verlas aisladas?
- ¿Cómo convertir datos oficiales dispersos en una vista clara, exportable y defendible?

## 5) Usuario objetivo inicial

1. El propio autor del proyecto.
2. Recruiters o evaluadores técnicos que quieran ver un proyecto serio y explicable.
3. Analistas o curiosos que valoren fuentes oficiales, reproducibilidad y exportación de reportes.

## 6) Recomendación de IDE

### Decisión principal
Usar **VS Code** como entorno principal durante el MVP.

### Motivo
- Ya existe continuidad de trabajo ahí.
- Gemini está siendo usado actualmente en VS Code.
- Reduce fricción de arranque.

### Cuándo reconsiderar PyCharm
Recién si el proyecto entra en una fase donde debugging, profiling o testing Python más pesado justifique cambiar de IDE.

## 7) Stack recomendado para el MVP

### Núcleo recomendado
- **Python 3.12+**
- **Streamlit** o **Taipy** para UI local rápida
- **Pandas** para transformación de datos
- **Polars** opcional si más adelante conviene por rendimiento
- **Plotly** para gráficos interactivos
- **DuckDB** o **SQLite** para snapshots, caché y persistencia local
- **Pydantic** para modelos/configuración
- **Requests** o **httpx** para conectores API
- **Pytest** para pruebas
- **Poetry** o **uv/pip-tools** para gestión de dependencias

### Stack a evitar al inicio
- React + FastAPI desde el día 1
- PostgreSQL remoto
- Microservicios
- Colas
- Autenticación de usuarios
- Forecasting complejo
- Infra cloud innecesaria

## 8) Fuentes de datos priorizadas

## Regla general
**API oficial primero.**
Si no existe API buena, usar descarga oficial pública.
Selenium solo entra en tercer lugar y únicamente de forma opcional y controlada.

### Fuentes principales del MVP

#### 1. World Bank Indicators API
**Rol:** base internacional abierta para benchmark país contra país.

**Ventajas:**
- abierta,
- estable,
- buena para indicadores macro de alto nivel,
- sin key en flujo base.

**Usos en el proyecto:**
- comparar Chile con países pares,
- traer series de inflación, PIB, desempleo u otros agregados,
- enriquecer paneles comparativos.

#### 2. FRED API
**Rol:** series económicas y financieras amplias, especialmente útiles como benchmark y referencia internacional.

**Ventajas:**
- catálogo muy amplio,
- documentación madura,
- muy buena para series temporales.

**Fricción:**
- requiere API key gratuita.

**Usos en el proyecto:**
- tasas,
- inflación,
- commodities,
- series macro de referencia.

#### 3. Banco Central de Chile (BCCh / BDE) — fase prioritaria si se logra acceso
**Rol:** fuente chilena fuerte para series económicas y monetarias locales.

**Ventajas:**
- alta relevancia para Chile,
- señal fuerte de seriedad si se integra.

**Fricción:**
- la credencial puede introducir algo más de fricción que World Bank.

**Usos en el proyecto:**
- tipo de cambio,
- tasas,
- actividad,
- indicadores monetarios.

#### 4. CMF — fase siguiente
**Rol:** datos financieros/regulatorios complementarios.

**Fricción:**
- API key,
- no debe entrar al núcleo del MVP si retrasa el avance.

#### 5. datos.gob.cl — fase siguiente / expansión
**Rol:** datasets públicos chilenos complementarios.

**Usos:**
- enriquecer contexto público local,
- integrar datasets auxiliares,
- alimentar futuras vistas tipo observatorio cívico/económico.

## 9) Decisión de fuentes para el MVP

### Obligatorias
- World Bank
- FRED

### Prioritaria si se consigue sin trabar el avance
- BCCh

### Fuera del núcleo inicial
- CMF
- datos.gob.cl como conector principal, salvo uso muy acotado

## 10) Qué debe hacer el MVP

### Capacidades mínimas
- Cargar un catálogo interno de series por categoría.
- Descargar datos desde al menos dos fuentes oficiales.
- Normalizar frecuencia y formato de fechas.
- Mostrar paneles comparativos por categoría.
- Permitir elegir benchmark o país de comparación.
- Generar una vista de resumen con variación reciente, tendencia simple y fuente utilizada.
- Exportar al menos un reporte local en CSV y uno en HTML o PDF.
- Mantener caché o snapshots locales para no golpear APIs innecesariamente.

### MVP cerrado sugerido
- Solo **8 a 12 series** al inicio.
- Solo **4 módulos visibles**: `Home`, `Series`, `Comparar`, `Reporte`.
- Solo **2 o 3 fuentes** conectadas.
- **Sin login**.
- **Sin scraping obligatorio**.
- **Sin forecast avanzado**.

## 11) Arquitectura base

El proyecto debe nacer **simple, modular y con fronteras claras**.

```text
macro-pulse-chile/
├─ app/
│  ├─ ui/
│  │  ├─ home.py
│  │  ├─ series.py
│  │  ├─ compare.py
│  │  └─ report.py
│  └─ main.py
├─ src/
│  ├─ connectors/
│  ├─ config/
│  ├─ domain/
│  ├─ services/
│  ├─ storage/
│  ├─ transform/
│  └─ utils/
├─ tests/
├─ docs/
├─ data/
│  ├─ raw/
│  ├─ processed/
│  └─ cache/
├─ notebooks/
├─ pyproject.toml
└─ README.md
```

### Responsabilidad por capas
- `connectors/`: hablar con APIs externas.
- `transform/`: limpieza, normalización, reshape, enriquecimiento.
- `domain/`: modelos de series, categorías, fuentes, reglas.
- `services/`: casos de uso agregados.
- `storage/`: snapshots, caché, persistencia local.
- `ui/`: interfaz y visualización, sin lógica pesada.

## 12) Orden recomendado de implementación

1. Crear estructura base del repo.
2. Definir config y catálogo de series.
3. Implementar conector World Bank.
4. Implementar conector FRED.
5. Normalizar fechas, frecuencias y nombres.
6. Crear storage local con snapshots/caché.
7. Armar vista `Series`.
8. Armar vista `Comparar`.
9. Armar vista `Reporte`.
10. Agregar exportación.
11. Recién después evaluar BCCh.

## 13) Reglas de trabajo para Gemini

- No ampliar scope sin justificarlo explícitamente.
- Antes de crear código nuevo, revisar el árbol del proyecto y la carpeta `docs/`.
- Mantener separadas las capas `connectors`, `transform`, `services` y `ui`.
- No meter lógica de negocio dentro de la UI.
- No cambiar nombres de series ni claves de config sin actualizar documentación y tests.
- Preferir cambios pequeños, trazables y revisables.
- Si una fuente tiene fricción de acceso, crear primero interfaz, modelo y stub.
- No bloquear el proyecto completo por una API secundaria.
- Registrar decisiones estructurales en `docs/adr-xxxx.md`.
- Cada conector debe tener pruebas con fixtures o respuestas sampleadas.
- Toda salida visible debe indicar fuente y fecha de actualización.

## 14) Rol correcto de Selenium

Macro Pulse Chile **no debe depender de Selenium como columna vertebral**.

### Selenium solo podría entrar de forma opcional para:
- descarga automatizada de archivos públicos cuando no exista API limpia,
- verificación periódica de cambios de estructura en una página pública,
- generación de evidencia visual de fuentes públicas.

### Regla dura
Usar Selenium solo sobre:
- recursos públicos,
- sin login,
- sin pago,
- sin evadir restricciones,
- y sin desplazar una API oficial que ya exista.

## 15) Riesgos principales y contención

### Riesgo 1: scope creep
**Contención:** limitar MVP a pocas series, pocas fuentes y pocas pantallas.

### Riesgo 2: atascarse con fuentes difíciles
**Contención:** priorizar World Bank y FRED; BCCh entra solo si no frena el avance.

### Riesgo 3: convertir el proyecto en un frontend gigante
**Contención:** UI local simple, sin SPA separada.

### Riesgo 4: mezclar demasiada lógica en una sola capa
**Contención:** respetar arquitectura modular desde el día 1.

## 16) Definición de terminado para la versión 0.1

La v0.1 está terminada si:
- el proyecto se instala y corre localmente sin pasos oscuros,
- descarga y guarda datos desde al menos dos fuentes,
- muestra gráficos y tablas útiles para al menos cuatro categorías macro,
- permite comparar Chile con uno o dos benchmarks,
- exporta un reporte local legible,
- tiene README serio,
- tiene estructura limpia,
- tiene pruebas mínimas funcionales.

## 17) Recomendación final

- Partir en **VS Code**.
- Mantener el proyecto **local-first**.
- Construir **primero el pipeline y después la visualización**.
- No abrir otro frente tipo frontend separado.
- No perseguir datos perfectos desde el día 1.
- Primero debe existir una base confiable, modular y demostrable.

## 18) Resumen ejecutivo en una línea

**Macro Pulse Chile debe nacer como un observatorio técnico sobrio, local, reproducible y explicable, no como una plataforma gigante.**

## 19) Roadmap Futuro (Post-MVP / v0.3+)

Con el MVP inicial (v0.2.0) completado y estable, las futuras iteraciones se enfocarán en profundizar el análisis y la calidad sin comprometer la arquitectura local-first.

### 1. Profundidad Analítica (Capa `transform` y `ui`)
- **Filtros Temporales Globales:** Controles en la barra lateral para recortar el análisis a ventanas específicas (ej. "Desde 2019").
- **Análisis de Tendencias (YoY / MoM):** Switches para visualizar variaciones porcentuales Interanuales (Year-over-Year) y Mensuales (Month-over-Month).
- **Suavizado de Curvas:** Implementación de promedios móviles (30/90 días) para indicadores de alta volatilidad (Tipo de Cambio, Cobre).

### 2. Expansión de Fronteras (Capa `connectors`)
- **datos.gob.cl / DIPRES:** Integración de ejecución presupuestaria u otros datasets cívicos.
- **Indicadores Laborales:** Búsqueda de fuentes oficiales para medir creación de empleo.
- **Mercados Financieros:** Explorar conectores (ej. `yfinance`) de forma aislada para comparar la economía real vs. índices bursátiles (IPSA, S&P 500).

### 3. Calidad de Software y DevOps
- **Integración Continua (CI):** Implementar GitHub Actions para ejecutar automáticamente la suite de Pytest en cada push.
- **Mantenimiento Local:** Crear un proceso de "recolección de basura" (Garbage Collection) para limpiar registros obsoletos en DuckDB y mantener la ligereza del proyecto.
