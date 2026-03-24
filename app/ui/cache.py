import streamlit as st
import pandas as pd
from src.services.data_manager import DataManager

@st.cache_data(show_spinner=False)
def get_cached_series(indicator_id: str) -> pd.DataFrame:
    """Envuelve la lectura de datos con la caché en memoria de Streamlit para evitar leer de disco en cada clic."""
    data_manager = DataManager()
    return data_manager.get_series_data(indicator_id)