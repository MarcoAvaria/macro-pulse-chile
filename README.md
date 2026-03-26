# Macro Pulse Chile 🇨🇱 📊

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Local_First-yellow.svg)](https://duckdb.org/)
[![Status](https://img.shields.io/badge/Estado-MVP_v0.1.0-brightgreen.svg)]()

**Macro Pulse Chile** es un observatorio macroeconómico **local-first** orientado a comparar la evolución económica de Chile contra pares y referencias internacionales, consumiendo exclusivamente **fuentes oficiales**.

Este proyecto fue construido con un enfoque estricto en **Arquitectura Limpia (Clean Architecture)**, separación de responsabilidades y optimización de rendimiento en memoria.

---

## 🚀 Características Principales

*   **Arquitectura Local-First:** Minimiza llamadas de red almacenando el histórico de series en una base de datos local **DuckDB**, garantizando persistencia y alta velocidad.
*   **Integración Multi-API:** Conectores modulares aislados para consumir datos desde:
    *   🏦 Banco Central de Chile (BCCh)
    *   🌐 The World Bank (Banco Mundial)
    *   🇺🇸 Federal Reserve Economic Data (FRED)
*   **Caché en Memoria RAM:** Uso intensivo de decoradores de Streamlit para evitar lecturas de disco iterativas, logrando una navegación instantánea (0 lag de repintado).
*   **Renderizado en Lotes (Batch Processing):** Procesamiento de transformaciones en Pandas aislado de la capa de Interfaz de Usuario para evitar saltos visuales en el frontend.
*   **Exportación Nativa:** Capacidad de normalizar series asimétricas, realizar *forward-fills* y exportar los datasets resultantes en formato `.csv` limpio.

---

## 🧠 Arquitectura del Sistema

El proyecto evita ser un "script gigante" dividiendo el código en dominios de responsabilidad estrictos:

```text
macro-pulse-chile/
├── app/
│   ├── ui/               # Vistas de Streamlit separadas por caso de uso.
│   └── cache.py          # Puente de caché en RAM. aislando UI de datos.
├── src/
│   ├── connectors/       # Clases API (FRED, World Bank, BCCh).
│   ├── config/           # Catálogo centralizado de indicadores macroeconómicos.
│   ├── domain/           # Modelos de datos estrictos usando Pydantic.
│   ├── services/         # DataManager: Orquestador de lógica de negocio.
│   └── storage/          # LocalStorage: Manejo de base de datos DuckDB.
├── main.py               # Punto de entrada y ruteo de la aplicación.
└── requirements.txt      # Dependencias congeladas para fácil reproducción.
