from src.config.catalog import get_catalog
from src.connectors.world_bank import WorldBankConnector

if __name__ == "__main__":
    catalog = get_catalog()
    wb = WorldBankConnector()
    
    # Tomamos la primera serie del catálogo (PIB de Chile)
    serie_pib = catalog[0]
    print(f"Descargando: {serie_pib.name} ({serie_pib.source_id})...")
    
    df = wb.fetch_series(indicator=serie_pib.source_id)
    print(df.tail()) # Mostrará los últimos 5 años de datos
