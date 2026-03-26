import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from unittest.mock import patch
from src.connectors.datos_gob import DatosGobConnector

@patch("src.connectors.datos_gob.requests.get")
def test_datos_gob_fetch_resource_success(mock_get):
    """Verifica que el conector CKAN extraiga los records tabulares correctamente."""
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "success": True,
        "result": {
            "records": [
                {"fecha": "2024-01-01", "partida": "Salud", "monto": 1000},
                {"fecha": "2024-02-01", "partida": "Salud", "monto": 1200}
            ]
        }
    }
    
    connector = DatosGobConnector()
    df = connector.fetch_resource("fake_resource_id")
    
    assert not df.empty
    assert len(df) == 2
    assert df.iloc[0]["monto"] == 1000