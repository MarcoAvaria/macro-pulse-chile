# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.
El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [0.2.0] - 2026-03-26

### Añadido (Added)
- **API CMF**: Nuevo conector para la Comisión para el Mercado Financiero, integrando la Unidad de Fomento (UF) y la Tasa Máxima Convencional (TMC).
- **Motor de Transformación**: Capa de normalización temporal con Pandas para alinear series diarias, mensuales y anuales mediante promedios.
- **Exportación HTML**: Generador nativo de reportes ejecutivos estáticos y descargables, listos para imprimir como PDF.
- **Testing Automatizado**: Suite de pruebas con Pytest para validar el catálogo de series y aplicar *mocking* al conector de la CMF.

### Mejorado (Changed)
- **Inteligencia de Unidades**: Las variaciones en el reporte ejecutivo ahora diferencian entre valores absolutos (mostrando variación porcentual relativa) y tasas de interés (mostrando diferencias en puntos porcentuales *pp*).
- **Limpieza de Datos**: La tabla comparativa ahora normaliza los datos (forward-fill) y se ajusta a la frecuencia seleccionada, eliminando lagunas visuales.

## [0.1.0] - 2026-03-24

### Añadido (Added)
- **Arquitectura Base**: Estructura modular separando UI, conectores, orquestación y persistencia local.
- **Conectores de Datos**: Integración con APIs oficiales de World Bank, FRED y Banco Central de Chile (BCCh).
- **Persistencia Local**: Base de datos local con DuckDB para almacenar y cachear el histórico de las series.
- **Catálogo Inicial**: 8 indicadores macroeconómicos clave (PIB, Inflación, Tasa FED, TPM Chile, Dólar, Cobre, IMACEC, Desempleo).
- **Interfaz de Usuario (UI)**:
  - **Vista Home**: Introducción y estado del proyecto.
  - **Vista Series**: Visualizador individual con gráficos interactivos Plotly.
  - **Vista Comparar**: Comparador múltiple con opciones de escalas independientes, originales y normalizadas a Base 100.
  - **Vista Reporte**: Dashboard ejecutivo con métricas automáticas calculadas respecto al periodo anterior.
- **Exportación**: Botón nativo para descargar la tabla de datos consolidados a formato `.csv`.
- **Optimización y UX**: 
  - Caché en memoria RAM de Streamlit para navegación instantánea entre pestañas.
  - Botón para destruir caché y forzar refresco desde las APIs oficiales.
  - Procesamiento por lotes (batch rendering) en UI para evitar repintados y saltos visuales.

### Mejorado (Changed)
- `requirements.txt` congelado con las dependencias exactas del entorno virtual para facilitar la instalación del proyecto.

### Arreglado (Fixed)
- Problemas de renderizado reactivo de Streamlit moviendo el procesamiento pesado de Pandas antes de inyectar componentes visuales.