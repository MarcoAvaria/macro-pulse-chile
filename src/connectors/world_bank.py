import requests
import pandas as pd
from typing import Optional

class WorldBankConnector:
    """Conector para la API oficial del Banco Mundial."""
    BASE_URL = "http://api.worldbank.org/v2"

    def __init__(self):
        # La API del Banco Mundial es abierta y no requiere API Key
        pass

    def fetch_series(
        self, 
        indicator: str, 
        country: str = "CL", 
        start_year: Optional[int] = None, 
        end_year: Optional[int] = None
    ) -> pd.DataFrame:
        """Descarga una serie desde la API y retorna un DataFrame estandarizado."""
        url = f"{self.BASE_URL}/country/{country}/indicator/{indicator}"
        
        params = {
            "format": "json",
            "per_page": 1000  # Intentamos traer la historia completa en una llamada
        }
        if start_year and end_year:
            params["date"] = f"{start_year}:{end_year}"

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # La respuesta del WB es una lista donde el índice 1 tiene los datos reales
        if len(data) < 2 or not data[1]:
            return pd.DataFrame()
            
        df = pd.DataFrame(data[1])
        df = df[['date', 'value']].rename(columns={'date': 'date_str'})
        df['indicator_id'] = indicator
        
        return df.dropna(subset=['value']).sort_values('date_str').reset_index(drop=True)