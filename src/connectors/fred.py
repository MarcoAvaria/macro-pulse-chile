import os
import requests
import pandas as pd
from typing import Optional

class FREDConnector:
    """Conector para la API del Federal Reserve Economic Data (FRED)."""
    BASE_URL = "https://api.stlouisfed.org/fred"

    def __init__(self, api_key: Optional[str] = None):
        # Intentamos obtener la key de los parámetros, sino del entorno local
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        if not self.api_key:
            raise ValueError("FRED_API_KEY no encontrada. Configúrala en el archivo .env")

    def fetch_series(
        self, 
        series_id: str, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """Descarga una serie desde FRED y retorna un DataFrame estandarizado."""
        url = f"{self.BASE_URL}/series/observations"
        
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
        }
        if start_date:
            params["observation_start"] = start_date
        if end_date:
            params["observation_end"] = end_date

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        observations = data.get("observations", [])
        if not observations:
            return pd.DataFrame()
            
        df = pd.DataFrame(observations)
        # FRED a veces envía un "." en vez de null para datos faltantes. Lo parseamos:
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        df = df[['date', 'value']].rename(columns={'date': 'date_str'})
        df['indicator_id'] = series_id
        
        return df.dropna(subset=['value']).sort_values('date_str').reset_index(drop=True)