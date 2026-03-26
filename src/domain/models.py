from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class DataSource(str, Enum):
    """Fuentes de datos permitidas en el MVP según PROJECT_CONTEXT.md"""
    WORLD_BANK = "world_bank"
    FRED = "fred"
    BCCH = "bcch"
    CMF = "cmf"
    DATOS_GOB = "datos_gob"

class Frequency(str, Enum):
    """Frecuencias de tiempo estandarizadas"""
    DAILY = "D"
    MONTHLY = "M"
    QUARTERLY = "Q"
    ANNUAL = "A"

class SeriesUnit(str, Enum):
    """Unidades de medida para dar contexto a los valores"""
    PERCENTAGE = "percentage"
    CURRENCY = "currency"
    INDEX = "index"

class SeriesConfig(BaseModel):
    """Modelo que define una serie macroeconómica a observar"""
    id: str = Field(..., description="ID interno en nuestro sistema (ej: 'cl_gdp_annual')")
    name: str = Field(..., description="Nombre legible para la UI")
    source: DataSource = Field(..., description="Fuente oficial de los datos")
    source_id: str = Field(..., description="ID exacto que usa la API de origen (ej: 'NY.GDP.MKTP.CD')")
    frequency: Frequency = Field(..., description="Frecuencia esperada")
    unit: SeriesUnit = Field(default=SeriesUnit.INDEX, description="Unidad de medida de la serie")
    description: Optional[str] = Field(default=None, description="Contexto opcional de la serie")