import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from unittest.mock import patch
from src.connectors.cmf import CMFConnector

def test_cmf_missing_api_key():
    """Verifica que el conector falle apropiadamente si no hay API Key."""
    with patch.dict(os.environ, clear=True):  # Limpiamos variables de entorno simuladamente
        with pytest.raises(ValueError, match="CMF_API_KEY no encontrada"):
            CMFConnector(api_key=None)

@patch("src.connectors.cmf.requests.get")
def test_cmf_fetch_series_success(mock_get):
    """Verifica que los datos de la CMF se limpien (ej: comas por puntos) y formen un DataFrame."""
    # Simulamos la respuesta JSON que enviaría la CMF
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "UFs": [
            {"Fecha": "2024-01-01", "Valor": "36.500,25"},
            {"Fecha": "2024-01-02", "Valor": "36.510,50"}
        ]
    }
    
    connector = CMFConnector(api_key="fake_key_para_test")
    df = connector.fetch_series("uf")
    
    # Validaciones estructurales
    assert not df.empty
    assert len(df) == 2
    assert list(df.columns) == ["date_str", "value", "indicator_id"]
    
    # Validación matemática (La limpieza del string)
    assert df.iloc[0]["value"] == 36500.25
    assert df.iloc[1]["value"] == 36510.5

@patch("src.connectors.cmf.requests.get")
def test_cmf_fetch_series_empty(mock_get):
    """Verifica que retorne un DataFrame vacío si la API responde sin datos."""
    mock_get.return_value.json.return_value = {"UFs": []}
    
    connector = CMFConnector(api_key="fake_key_para_test")
    df = connector.fetch_series("uf")
    
    assert isinstance(df, pd.DataFrame)
    assert df.empty