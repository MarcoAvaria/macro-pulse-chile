import streamlit as st
import pandas as pd
from src.config.catalog import get_catalog
from app.ui.cache import get_cached_series
from src.domain.models import SeriesUnit
from datetime import datetime

def render_report_page():
    
    # 1. FASE DE CÁLCULO (Absolutamente todo el procesamiento de datos antes de dibujar)
    catalog = get_catalog()
    metricas = []
    for serie_config in catalog:
        df = get_cached_series(serie_config.source_id)
        
        if not df.empty:
            df_temp = df.copy() # Evitamos modificar la caché
            df_temp['date'] = pd.to_datetime(df_temp['date_str'], format='mixed')
            
            # Aplicar filtro temporal global
            start_year = st.session_state.get('start_year', 2010)
            df_temp = df_temp[df_temp['date'].dt.year >= start_year]
            
            df_temp = df_temp.sort_values('date')
            
            if len(df_temp) >= 2:
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

    # 3. FASE DE EXPORTACIÓN (Reporte Estático)
    st.divider()
    st.subheader("📥 Exportar Reporte")
    st.write("Descarga una versión estática de este reporte para compartir o visualizar offline.")

    # Generar tarjetas HTML usando código limpio
    html_cards = ""
    for m in metricas:
        # Determinar color rudimentario basado en el signo + o -
        color = "green" if "+" in m['delta'] else ("red" if "-" in m['delta'] else "gray")
        
        html_cards += f"""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; min-width: 250px; flex: 1; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); font-family: sans-serif;">
            <div style="font-size: 0.9em; color: #666; margin-bottom: 8px;">{m['label']}</div>
            <div style="font-size: 1.8em; font-weight: bold; margin-bottom: 8px; color: #222;">{m['value']}</div>
            <div style="font-size: 1em; color: {color}; margin-bottom: 15px;">{m['delta']}</div>
            <div style="font-size: 0.8em; color: #999; border-top: 1px solid #eee; padding-top: 10px;">{m['help']}</div>
        </div>
        """

    # Ensamblar HTML completo
    fecha_generacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte Ejecutivo - Macro Pulse Chile</title>
    </head>
    <body style="font-family: Arial, sans-serif; margin: 40px; color: #333; max-width: 1200px; margin-left: auto; margin-right: auto;">
        <h1 style="color: #0056b3;">📑 Reporte Ejecutivo - Macro Pulse Chile</h1>
        <p>Resumen consolidado de indicadores macroeconómicos locales e internacionales.</p>
        <p style="font-size: 0.9em; color: #666;">Generado el: <strong>{fecha_generacion}</strong></p>
        
        <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 30px;">
            {html_cards}
        </div>
    </body>
    </html>
    """

    st.download_button(
        label="📄 Descargar Reporte (HTML)",
        data=html_content,
        file_name=f"Macro_Pulse_Reporte_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html"
    )