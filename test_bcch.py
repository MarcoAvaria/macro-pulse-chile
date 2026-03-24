import os
from dotenv import load_dotenv
from src.connectors.bcch import BCChConnector

load_dotenv()

if __name__ == "__main__":
    try:
        bcch = BCChConnector()
        
        # Código oficial del BCCh para la Tasa de Política Monetaria (TPM)
        serie_tpm = "F022.TPM.TIN.D001.NO.Z.D"
        
        print(f"Descargando datos desde BCCh (Serie TPM: {serie_tpm})...")
        
        # Traemos datos desde 2024 para no demorar la prueba
        df = bcch.fetch_series(serie_tpm, start_date="2024-01-01")
        
        if not df.empty:
            print("✅ Conexión exitosa al Banco Central. Últimos datos:")
            print(df.tail())
        else:
            print("⚠️ Conexión exitosa, pero no se recibieron datos.")
            
    except ValueError as e:
        print(f"❌ Error detectado:\n{e}")
        print("\n💡 Recuerda que debes configurar BCCH_USER y BCCH_PASS en tu archivo .env.")
        print("👉 Si no tienes cuenta, créala gratis en: https://bde.bcentral.cl/bde/es/Estadisticas/Suscripcion")