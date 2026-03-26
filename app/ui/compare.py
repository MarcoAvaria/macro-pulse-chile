import streamlit as st
import plotly.express as px
import pandas as pd
from src.config.catalog import get_catalog
from app.ui.cache import get_cached_series
from src.transform.frequencies import normalize_frequency
from src.transform.variations import calculate_variation

def render_compare_page():
    st.title("⚖️ Comparador de Series")
    st.write("Selecciona múltiples indicadores para observar su evolución conjunta.")

    catalog = get_catalog()

    # Diccionario: nombre bonito -> source_id
    opciones = {s.name: s.source_id for s in catalog}
    
    selecciones = st.multiselect(
        "Añade indicadores al gráfico:", 
        list(opciones.keys())
    )

    modo_vis = st.radio(
        "Modo de visualización:",
        [
            "Gráficos separados (Escalas independientes)",
            "Gráfico único (Normalizado a Base 100)",
            "Gráfico único (Escalas originales)"
        ]
    )
    
    frecuencia = st.radio(
        "Normalizar frecuencia temporal:",
        options=["Diaria (Original)", "Mensual (Promedio)", "Anual (Promedio)"],
        horizontal=True
    )
    freq_dict = {"Diaria (Original)": "D", "Mensual (Promedio)": "M", "Anual (Promedio)": "A"}
    
    tipo_valor = st.radio(
        "Análisis de Tendencia:",
        options=["Valor Absoluto", "MoM (Variación Mensual %)", "YoY (Variación Interanual %)"],
        horizontal=True
    )

    if selecciones:
        df_lista = []
        
        for nombre in selecciones:
            source_id = opciones[nombre]
            # Usamos .copy() para no modificar el caché en memoria si lo hubiera
            df_temp = get_cached_series(source_id).copy()
            if not df_temp.empty:
                df_temp['Indicador'] = nombre
                df_lista.append(df_temp)

        if df_lista:
            df_final = pd.concat(df_lista, ignore_index=True)
            
            # 1. Convertir strings a fechas reales para alinear frecuencias
            df_final['date'] = pd.to_datetime(df_final['date_str'], format='mixed')
            
            # Aplicar filtro temporal global
            start_year = st.session_state.get('start_year', 2010)
            df_final = df_final[df_final['date'].dt.year >= start_year]

            # 2. Aplicar capa de transformación
            df_final = normalize_frequency(df_final, freq_dict[frecuencia])
            
            # 3. Aplicar variación si se solicita
            if tipo_valor != "Valor Absoluto":
                df_final = calculate_variation(df_final, tipo_valor)
                st.info(f"💡 Se aplicó la transformación matemática **{tipo_valor}**. La frecuencia fue ajustada a Mensual automáticamente para el cálculo.", icon="ℹ️")
            
            if modo_vis == "Gráfico único (Normalizado a Base 100)":
                # Ordenar cronológicamente para asegurar que el cálculo tome el primer dato real
                df_final = df_final.sort_values(['Indicador', 'date'])
                
                # Lógica: (Valor_Actual / Primer_Valor) * 100
                # Así igualamos el punto de partida de todas las series.
                df_final['value'] = df_final.groupby('Indicador')['value'].transform(lambda x: (x / x.iloc[0]) * 100)
                
                fig = px.line(
                    df_final, x="date", y="value", color="Indicador", markers=True,
                    title="Comparación de Tendencias (Base 100 = Inicio de la serie)"
                )
                st.plotly_chart(fig, width="stretch")
                st.info("💡 En Base 100 todas las series inician en el mismo punto. Es ideal para ver variaciones porcentuales relativas sin que se rompa el gráfico.", icon="📊")
                
            elif modo_vis == "Gráfico único (Escalas originales)":
                fig = px.line(
                    df_final, x="date", y="value", color="Indicador", markers=True,
                    title="Comparación de Series (Escalas Originales Mixtas)"
                )
                st.plotly_chart(fig, width="stretch")
                st.warning("⚠️ Precaución: Al mezclar escalas tan diferentes (ej. millones vs porcentajes) en un solo gráfico, las series con valores menores pueden verse planas.", icon="⚠️")
                
            else: # "Gráficos separados (Escalas independientes)"
                # Comportamiento: subgráficos apilados
                altura_dinamica = max(400, 250 * len(selecciones))
                fig = px.line(
                    df_final, x="date", y="value", color="Indicador", 
                    facet_row="Indicador", markers=True, height=altura_dinamica
                )
                
                # Liberar el eje Y para que cada subgráfico tenga su propia escala
                fig.update_yaxes(matches=None, showticklabels=True)
                fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
                
                st.plotly_chart(fig, width="stretch")
                st.info("💡 Las series comparten el eje temporal (X), pero usan escalas verticales (Y) absolutas e independientes.", icon="⚖️")

            # Agregar tabla de datos debajo de los gráficos
            st.divider()
            st.subheader("📋 Datos Históricos")
            
            # Pivotar para lectura humana: Fechas como filas, Indicadores como columnas
            df_pivot = df_final.pivot_table(index='date', columns='Indicador', values='value')
            
            # Rellenar vacíos: ordenar cronológicamente, aplicar forward-fill y volver a invertir
            df_pivot = df_pivot.sort_index(ascending=True)
            df_pivot = df_pivot.ffill()
            
            df_pivot.index = df_pivot.index.strftime('%Y-%m-%d')
            df_pivot = df_pivot.sort_index(ascending=False) # Más recientes primero
            
            # Formatear la tabla visualmente: 2 decimales y ocultar vacíos (NaN/None)
            st.dataframe(df_pivot.style.format(precision=2, na_rep="-"), width="stretch")
            
            # Botón nativo de exportación a CSV
            csv = df_pivot.to_csv().encode('utf-8')
            st.download_button(
                label="📥 Descargar datos (CSV)",
                data=csv,
                file_name="comparacion_macro_pulse.csv",
                mime="text/csv",
            )