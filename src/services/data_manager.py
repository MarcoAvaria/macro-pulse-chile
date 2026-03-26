import pandas as pd
from datetime import datetime
from src.config.catalog import get_catalog
from src.connectors.world_bank import WorldBankConnector
from src.connectors.fred import FREDConnector
from src.connectors.bcch import BCChConnector
from src.connectors.cmf import CMFConnector
from src.storage.local_db import LocalStorage
from src.domain.models import DataSource

class DataManager:
    """Orquestador: Decide si leer de la base de datos local o ir a las APIs."""
    
    def __init__(self):
        self.catalog = get_catalog()
        self.db = LocalStorage()
        self.wb = WorldBankConnector()
        self.fred = FREDConnector()
        self.bcch = BCChConnector()
        self.cmf = CMFConnector()

    def get_series_data(self, indicator_id: str) -> pd.DataFrame:
        """Retorna los datos de una serie, priorizando la base de datos local."""
        # 1. Intentar leer de la caché local (DuckDB)
        df = self.db.get_series(indicator_id)
        if not df.empty:
            return df
            
        # 2. Si no hay datos, buscar en el catálogo para saber de dónde descargarlos
        serie_config = next((s for s in self.catalog if s.source_id == indicator_id), None)
        if not serie_config:
            raise ValueError(f"Serie {indicator_id} no configurada en el catálogo.")

        # 3. Descargar usando el conector adecuado
        if serie_config.source == DataSource.WORLD_BANK:
            df = self.wb.fetch_series(serie_config.source_id)
        elif serie_config.source == DataSource.FRED:
            df = self.fred.fetch_series(serie_config.source_id)
        elif serie_config.source == DataSource.BCCH:
            # Limitamos a partir del 2010 para que sea rápido y no traer décadas de datos diarios
            df = self.bcch.fetch_series(serie_config.source_id, start_date="2010-01-01")
        elif serie_config.source == DataSource.CMF:
            # Limitamos el rango para no sobrecargar la API de CMF
            df = self.cmf.fetch_series(serie_config.source_id, start_date="2023-01-01", end_date=datetime.now().strftime("%Y-%m-%d"))

        # 4. Guardar en DuckDB para futuras consultas y retornar
        if not df.empty:
            self.db.save_series(df, indicator_id)
        return df

    def clear_local_data(self):
        """Limpia la persistencia local para forzar la actualización desde las APIs."""
        self.db.clear_all_series()