from src.domain.models import SeriesConfig, DataSource, Frequency

DEFAULT_CATALOG = [
    SeriesConfig(
        id="cl_gdp_annual",
        name="PIB (US$ a precios actuales)",
        source=DataSource.WORLD_BANK,
        source_id="NY.GDP.MKTP.CD",
        frequency=Frequency.ANNUAL,
        description="Producto Interno Bruto de Chile"
    ),
    SeriesConfig(
        id="cl_inflation_annual",
        name="Inflación, precios al consumidor (% anual)",
        source=DataSource.WORLD_BANK,
        source_id="FP.CPI.TOTL.ZG",
        frequency=Frequency.ANNUAL,
        description="Inflación anual basada en el IPC"
    ),
    SeriesConfig(
        id="us_fed_funds",
        name="Tasa de Fondos Federales (EE.UU.)",
        source=DataSource.FRED,
        source_id="FEDFUNDS",
        frequency=Frequency.MONTHLY,
        description="Tasa de interés de referencia de la Reserva Federal"
    ),
    SeriesConfig(
        id="tpm_chile",
        name="Tasa de Política Monetaria (Chile)",
        source=DataSource.BCCH,
        source_id="F022.TPM.TIN.D001.NO.Z.D",
        frequency=Frequency.DAILY,
        description="Tasa de política monetaria (TPM) fijada por el Banco Central de Chile."
    ),
    SeriesConfig(
        id="cl_exchange_rate_usd",
        name="Tipo de Cambio (Dólar Observado)",
        source=DataSource.BCCH,
        source_id="F073.TCO.PRE.Z.D",
        frequency=Frequency.DAILY,
        description="Valor diario del dólar observado publicado por el Banco Central."
    ),
    SeriesConfig(
        id="cl_imacec",
        name="IMACEC (Índice Mensual de Actividad Económica)",
        source=DataSource.BCCH,
        source_id="F032.IMC.IND.Z.Z.EP18.Z.Z.0.M",
        frequency=Frequency.MONTHLY,
        description="Indicador que resume la actividad de los distintos sectores de la economía chilena en un mes determinado."
    ),
    SeriesConfig(
        id="global_copper_price",
        name="Precio Global del Cobre (US$ por Tonelada)",
        source=DataSource.FRED,
        source_id="PCOPPUSDM",
        frequency=Frequency.MONTHLY,
        description="Precio internacional del cobre. Benchmark global del FMI."
    ),
    SeriesConfig(
        id="cl_unemployment_annual",
        name="Desempleo (% de la fuerza laboral)",
        source=DataSource.WORLD_BANK,
        source_id="SL.UEM.TOTL.ZS",
        frequency=Frequency.ANNUAL,
        description="Tasa de desempleo total en Chile (estimación modelada OIT)."
    )
]

def get_catalog() -> list[SeriesConfig]:
    """Retorna el catálogo base de series activas en el MVP."""
    return DEFAULT_CATALOG