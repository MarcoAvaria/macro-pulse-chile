import pandas as pd
from src.transform.frequencies import normalize_frequency

def calculate_variation(df: pd.DataFrame, tipo: str) -> pd.DataFrame:
    """
    Aplica el cálculo de variación porcentual a un DataFrame.
    tipo: 'Valor Absoluto', 'MoM (Variación Mensual %)', 'YoY (Variación Interanual %)'
    """
    if df.empty or tipo == "Valor Absoluto":
        return df
        
    df_copy = df.copy()
    group_col = 'Indicador' if 'Indicador' in df_copy.columns else 'indicator_id'
    
    # 1. Normalizar a frecuencia mensual para evitar saltos de fin de semana
    # y asegurar que periods=1 sea exactamente un mes, y periods=12 un año.
    df_norm = normalize_frequency(df_copy, "M")
    
    result = []
    for indicador, group in df_norm.groupby(group_col):
        group = group.sort_values('date')
        
        # 2. pct_change calcula la variación respecto a 'n' periodos atrás
        if "MoM" in tipo:
            group['value'] = group['value'].pct_change(periods=1) * 100
        elif "YoY" in tipo:
            group['value'] = group['value'].pct_change(periods=12) * 100
            
        group = group.dropna(subset=['value'])
        result.append(group)
        
    return pd.concat(result, ignore_index=True) if result else df_norm