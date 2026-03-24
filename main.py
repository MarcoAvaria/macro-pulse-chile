import streamlit as st
from app.ui.series import render_series_page
from app.ui.compare import render_compare_page
from app.ui.report import render_report_page
from app.ui.cache import get_cached_series
from src.services.data_manager import DataManager
from dotenv import load_dotenv

# Cargar variables de entorno al iniciar la aplicación
load_dotenv(override=True)

def render_home():
    st.title("Macro Pulse Chile 🇨🇱")
    st.write("Observatorio macroeconómico local-first orientado a comparar a Chile contra pares internacionales.")
    st.info("🚧 Versión 0.1 en desarrollo - Fuentes oficiales y gratuitas.", icon="ℹ️")

def main():
    st.set_page_config(page_title="Macro Pulse Chile", layout="wide")
    
    # Menú lateral simple para el MVP
    menu = ["Inicio", "Series", "Comparar", "Reporte"]
    eleccion = st.sidebar.selectbox("Navegación", menu)

    # Botón para refrescar la base de datos
    st.sidebar.divider()
    if st.sidebar.button("🔄 Forzar Actualización", help="Borra la base local y descarga los datos de nuevo."):
        DataManager().clear_local_data()
        get_cached_series.clear() # Limpia la memoria RAM de Streamlit
        st.sidebar.success("Caché borrada. Los datos se recargarán al navegar.")

    if eleccion == "Inicio":
        render_home()
    elif eleccion == "Series":
        render_series_page()
    elif eleccion == "Comparar":
        render_compare_page()
    elif eleccion == "Reporte":
        render_report_page()
    else:
        st.warning(f"La vista '{eleccion}' está en construcción.")

if __name__ == "__main__":
    main()