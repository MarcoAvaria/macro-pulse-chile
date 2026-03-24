import os
from dotenv import load_dotenv
from src.config.catalog import get_catalog
from src.connectors.fred import FREDConnector
from src.storage.local_db import LocalStorage

load_dotenv()

if __name__ == "__main__":
    catalog = get_catalog()
    fred = FREDConnector()
    db = LocalStorage()

    # 1. Buscamos la serie en el catálogo
    serie_fed = next(s for s in catalog if s.source_id == "FEDFUNDS")
    print(f"1. Descargando datos de FRED: {serie_fed.name}...")
    df_descargado = fred.fetch_series(series_id=serie_fed.source_id)
    
    # 2. Guardamos en la base de datos local
    print("2. Guardando en DuckDB...")
    db.save_series(df_descargado, serie_fed.source_id)
    
    # 3. Leemos directamente desde la base de datos (simulando lo que hará Streamlit)
    print("3. Leyendo desde DuckDB local:")
    df_local = db.get_series(serie_fed.source_id)
    print(df_local.tail())
