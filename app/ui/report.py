import streamlit as st
import pandas as pd
from src.config.catalog import get_catalog
from app.ui.cache import get_cached_series
from src.domain.models import SeriesUnit

def render_report_page():
    
    # 1. FASE DE CÁLCULO (Absolutamente todo el procesamiento de datos antes de dibujar)
    catalog = get_catalog()
    metricas = []
    for serie_config in catalog:
        df = get_cached_series(serie_config.source_id)
        
        if not df.empty and len(df) >= 2:
            df_temp = df.copy() # Evitamos modificar la caché
            df_temp['date'] = pd.to_datetime(df_temp['date_str'], format='mixed')
            df_temp = df_temp.sort_values('date')
            
            ultimo = df_temp.iloc[-1]
            penultimo = df_temp.iloc[-2]
            
            variacion = ultimo['value'] - penultimo['value']
            fecha_corta = ultimo['date'].strftime('%b %Y')
            
            if serie_config.unit == SeriesUnit.PERCENTAGE:
                # Tasas de interés o inflación: variación en puntos porcentuales (pp)
                delta_str = f"{variacion:+.2f} pp vs ant."
            else:
                # Valores absolutos: crecimiento porcentual relativo
                pct_variacion = (variacion / penultimo['value']) * 100 if penultimo['value'] != 0 else 0.0
                delta_str = f"{variacion:+,.2f} ({pct_variacion:+.2f}%) vs ant."

            metricas.append({
                "label": f"{serie_config.name} ({fecha_corta})",
                "value": f"{ultimo['value']:,.2f}",
                "delta": delta_str,
                "help": f"Fuente: {serie_config.source.value.upper()} | ID: {serie_config.source_id}"
            })
    
    # 2. FASE DE DIBUJO (Se envía todo el HTML junto en milisegundos sin interrupciones)
    st.title("📑 Reporte Ejecutivo")
    st.write("Resumen de la situación actual y variaciones de los indicadores monitoreados.")
    
    st.info("💡 Este reporte consolida automáticamente el último dato de la base local. Los valores en verde/rojo indican la dirección del cambio, no necesariamente si es bueno o malo económicamente.", icon="🤖")
    st.divider()

    st.subheader("Últimos datos disponibles")
    
    cols = st.columns(3)
    for idx, m in enumerate(metricas):
        col = cols[idx % 3]
        col.metric(label=m["label"], value=m["value"], delta=m["delta"], help=m["help"])