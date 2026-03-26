import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from src.connectors.cmf import CMFConnector

load_dotenv()

if __name__ == "__main__":
    try:
        cmf = CMFConnector()
        
        # Recurso de prueba: Unidad de Fomento (UF)
        serie_uf = "uf"
        
        print(f"Descargando datos desde CMF (Serie: {serie_uf})...")
        
        # Probamos traer datos del año actual
        df = cmf.fetch_series(serie_uf)
        
        if not df.empty:
            print("✅ Conexión exitosa a la CMF. Últimos datos de la UF:")
            print(df.tail())
    except ValueError as e:
        print(f"❌ Error detectado:\n{e}")
        print("\n💡 Obtén tu API Key gratis en: https://api.cmfchile.cl/")