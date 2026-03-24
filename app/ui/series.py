import streamlit as st
import plotly.express as px
import pandas as pd
from src.config.catalog import get_catalog
from app.ui.cache import get_cached_series

def render_series_page():
    st.title("📈 Visualizador de Series")
    st.write("Consulta el histórico de los indicadores macroeconómicos.")

    catalog = get_catalog()

    # Diccionario para mostrar el nombre bonito en la UI pero usar el ID por debajo
    opciones = {s.name: s.source_id for s in catalog}
    seleccion = st.selectbox("Selecciona un indicador:", list(opciones.keys()))
    
    if seleccion:
        source_id = opciones[seleccion]
        
        df = get_cached_series(source_id)

        if not df.empty:
            # Gráfico interactivo con Plotly
            df_plot = df.copy()
            df_plot['date'] = pd.to_datetime(df_plot['date_str'], format='mixed')
            
            fig = px.line(df_plot, x="date", y="value", title=seleccion, markers=True)
            st.plotly_chart(fig, width="stretch")