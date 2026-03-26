import requests
import pandas as pd

class DatosGobConnector:
    """
    Conector para la API de datos.gob.cl (CKAN).
    Utilizado para consultar datasets cívicos como DIPRES (Presupuesto).
    """
    BASE_URL = "https://datos.gob.cl/api/3/action"

    def fetch_resource(self, resource_id: str, limit: int = 100) -> pd.DataFrame:
        """
        Descarga registros desde un recurso tabular (DataStore) en CKAN.
        Nota: CKAN retorna tablas con múltiples columnas. Cada dataset 
        requerirá una transformación específica en src/transform/ para 
        convertirlo al formato estándar de serie de tiempo (date_str, value).
        """
        url = f"{self.BASE_URL}/datastore_search"
        params = {"resource_id": resource_id, "limit": limit}
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("success", False):
            raise ValueError(f"Error en datos.gob.cl: {data.get('error')}")
            
        records = data.get("result", {}).get("records", [])
        return pd.DataFrame(records) if records else pd.DataFrame()