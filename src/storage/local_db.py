import duckdb
import pandas as pd
from pathlib import Path

# Guardaremos la base de datos en la carpeta que creamos para esto
DB_PATH = Path("data/processed/macro_data.duckdb")

class LocalStorage:
    """Maneja la persistencia local de las series usando DuckDB."""
    
    def __init__(self, db_path: str | Path = DB_PATH):
        self.db_path = str(db_path)
        self._init_db()

    def _init_db(self):
        """Crea la tabla base si no existe."""
        with duckdb.connect(self.db_path) as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS macro_series (
                    date_str VARCHAR,
                    value DOUBLE,
                    indicator_id VARCHAR
                )
            """)

    def save_series(self, df: pd.DataFrame, indicator_id: str):
        """Guarda un DataFrame en DuckDB, reemplazando los datos previos de esa serie."""
        if df.empty:
            return
            
        with duckdb.connect(self.db_path) as con:
            # Borramos los datos viejos de este indicador para evitar duplicados al actualizar
            con.execute("DELETE FROM macro_series WHERE indicator_id = ?", (indicator_id,))
            # DuckDB permite leer un DataFrame de Pandas directamente desde la variable local 'df'
            con.execute("INSERT INTO macro_series SELECT date_str, value, indicator_id FROM df")

    def get_series(self, indicator_id: str) -> pd.DataFrame:
        """Recupera la historia completa de un indicador."""
        with duckdb.connect(self.db_path) as con:
            return con.execute(
                "SELECT * FROM macro_series WHERE indicator_id = ? ORDER BY date_str", 
                (indicator_id,)
            ).df()

    def clear_all_series(self):
        """Borra todos los registros para forzar una nueva descarga."""
        with duckdb.connect(self.db_path) as con:
            con.execute("DELETE FROM macro_series")