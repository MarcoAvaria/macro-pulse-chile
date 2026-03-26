import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from src.config.catalog import get_catalog
from src.connectors.fred import FREDConnector

# Cargar el .env antes de inicializar el conector
load_dotenv()

if __name__ == "__main__":
    catalog = get_catalog()
    fred = FREDConnector()

    # Extraer la serie del FRED que agregamos
    serie_fed = next(s for s in catalog if s.source_id == "FEDFUNDS")
    print(f"Descargando: {serie_fed.name} ({serie_fed.source_id})...")

    df = fred.fetch_series(series_id=serie_fed.source_id)
    print(df.tail())
