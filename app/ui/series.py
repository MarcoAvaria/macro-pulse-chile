import streamlit as st
import plotly.express as px
import pandas as pd
from src.config.catalog import get_catalog
from app.ui.cache import get_cached_series
from src.transform.variations import calculate_variation

def render_series_page():
    st.title("📈 Visualizador de Series")
    st.write("Consulta el histórico de los indicadores macroeconómicos.")

    catalog = get_catalog()

    # Diccionario para mostrar el nombre bonito en la UI pero usar el ID por debajo
    opciones = {s.name: s.source_id for s in catalog}
    seleccion = st.selectbox("Selecciona un indicador:", list(opciones.keys()))
    
    tipo_valor = st.radio(
        "Análisis de Tendencia:",
        options=["Valor Absoluto", "MoM (Variación Mensual %)", "YoY (Variación Interanual %)"],
        horizontal=True
    )

    if seleccion:
        source_id = opciones[seleccion]
        
        df = get_cached_series(source_id)

        if not df.empty:
            # Gráfico interactivo con Plotly
            df_plot = df.copy()
            df_plot['date'] = pd.to_datetime(df_plot['date_str'], format='mixed')
            
            # Aplicar filtro temporal global
            start_year = st.session_state.get('start_year', 2010)
            df_plot = df_plot[df_plot['date'].dt.year >= start_year]
            
            # Aplicar transformaciones analíticas
            df_plot = calculate_variation(df_plot, tipo_valor)

            titulo = seleccion if tipo_valor == "Valor Absoluto" else f"{seleccion} - {tipo_valor}"
            fig = px.line(df_plot, x="date", y="value", title=titulo, markers=True)
            st.plotly_chart(fig, width="stretch")