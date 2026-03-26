import os
import requests
import pandas as pd
from typing import Optional
from datetime import datetime

class CMFConnector:
    """Conector para la API de la Comisión para el Mercado Financiero (CMF - ex SBIF)."""
    BASE_URL = "https://api.cmfchile.cl/api-sbifv3/recursos_api"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CMF_API_KEY")
        if not self.api_key:
            raise ValueError("CMF_API_KEY no encontrada. Configúrala en el archivo .env")

    def fetch_series(
        self, 
        series_id: str, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Descarga una serie desde la CMF.
        series_id: recurso a consultar (ej: 'uf', 'tmc', 'dolar')
        """
        if start_date and end_date:
            sd = pd.to_datetime(start_date)
            ed = pd.to_datetime(end_date)
            # Endpoint de período: /recursos_api/{recurso}/periodo/{yyyy}/{mm}/{yyyy}/{mm}
            url = f"{self.BASE_URL}/{series_id}/periodo/{sd.year}/{sd.month:02d}/{ed.year}/{ed.month:02d}"
        else:
            # Default: Endpoint del año actual
            year = datetime.now().year
            url = f"{self.BASE_URL}/{series_id}/{year}"

        params = {
            "apikey": self.api_key,
            "formato": "json"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Buscamos la lista de datos dinámicamente ('UFs', 'Dolares', etc.)
        records = next((v for k, v in data.items() if isinstance(v, list)), [])
        if not records:
            return pd.DataFrame()
            
        parsed_records = []
        for row in records:
            # CMF devuelve Valor como "36.500,25", hay que limpiarlo a "36500.25"
            valor_str = row.get("Valor", "").replace(".", "").replace(",", ".")
            if row.get("Fecha") and valor_str:
                parsed_records.append({"date_str": row.get("Fecha"), "value": float(valor_str), "indicator_id": series_id})
                
        df = pd.DataFrame(parsed_records)
        return df.sort_values("date_str").reset_index(drop=True)