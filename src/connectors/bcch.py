import os
import requests
import pandas as pd
from typing import Optional

class BCChConnector:
    """Conector para la API del Banco Central de Chile (BDE - SieteRestWS)."""
    BASE_URL = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"

    def __init__(self, user: Optional[str] = None, password: Optional[str] = None):
        self.user = user or os.getenv("BCCH_USER")
        self.password = password or os.getenv("BCCH_PASS")
        
        if not self.user or not self.password:
            raise ValueError("Credenciales BCCh no encontradas. Configura BCCH_USER y BCCH_PASS en tu archivo .env")

    def fetch_series(
        self, 
        series_id: str, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """Descarga una serie desde el BCCh y retorna un DataFrame estandarizado."""
        params = {
            "user": self.user,
            "pass": self.password,
            "timeseries": series_id,
            "function": "GetSeries"
        }
        
        if start_date:
            params["firstdate"] = start_date
        if end_date:
            params["lastdate"] = end_date

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # BCCh devuelve Codigo 0 cuando es exitoso
        if data.get("Codigo") != 0:
            raise ValueError(f"Error de BCCh API: {data.get('Descripcion')}")
            
        observaciones = data.get("Series", {}).get("Obs", [])
        if not observaciones:
            return pd.DataFrame()

        records = []
        for obs in observaciones:
            fecha_str = obs.get("indexDateString") # Viene en formato dd-MM-yyyy
            valor_str = obs.get("value")
            
            if fecha_str and valor_str and str(valor_str).strip().lower() != "nan":
                # Convertimos la fecha de Chile (DD-MM-YYYY) a formato internacional (YYYY-MM-DD)
                fecha_std = pd.to_datetime(fecha_str, format="%d-%m-%Y").strftime("%Y-%m-%d")
                records.append({"date_str": fecha_std, "value": float(valor_str), "indicator_id": series_id})

        df = pd.DataFrame(records)
        return df.sort_values("date_str").reset_index(drop=True)