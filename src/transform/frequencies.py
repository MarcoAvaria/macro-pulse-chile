import pandas as pd

def normalize_frequency(df: pd.DataFrame, freq: str) -> pd.DataFrame:
    """
    Normaliza la frecuencia temporal de un DataFrame con múltiples indicadores.
    freq: 'D' (Diario), 'M' (Mensual), 'A' (Anual)
    """
    if df.empty or freq == 'D':
        return df

    df_copy = df.copy()
    
    # Mapeo a las frecuencias modernas de Pandas (Month-End, Year-End)
    freq_map = {'M': 'ME', 'A': 'YE'}
    pd_freq = freq_map.get(freq, freq)

    result = []
    # Identificamos la columna a usar para agrupar dinámicamente
    group_col = 'Indicador' if 'Indicador' in df_copy.columns else 'indicator_id'
    
    for indicador, group in df_copy.groupby(group_col):
        # Convertimos la fecha en índice, resampleamos y calculamos el promedio
        resampled = group.set_index('date').resample(pd_freq)['value'].mean().reset_index()
        resampled[group_col] = indicador
        
        # Eliminamos meses/años vacíos que Pandas haya podido generar en el resampleo
        resampled = resampled.dropna(subset=['value'])
        result.append(resampled)
        
    return pd.concat(result, ignore_index=True) if result else df_copy