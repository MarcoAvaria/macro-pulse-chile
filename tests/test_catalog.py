import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.config.catalog import get_catalog
from src.domain.models import SeriesConfig, DataSource

def test_get_catalog_returns_list():
    """Verifica que el catálogo se cargue y no esté vacío."""
    catalog = get_catalog()
    assert isinstance(catalog, list)
    assert len(catalog) > 0

def test_catalog_contains_valid_models():
    """Verifica que todos los elementos sean instancias válidas de Pydantic."""
    catalog = get_catalog()
    for item in catalog:
        assert isinstance(item, SeriesConfig)
        assert isinstance(item.source, DataSource)

def test_catalog_has_required_series():
    """Verifica que indicadores críticos existan en la configuración."""
    catalog = get_catalog()
    ids = [item.id for item in catalog]
    assert "cl_gdp_annual" in ids
    assert "us_fed_funds" in ids
    assert "tpm_chile" in ids