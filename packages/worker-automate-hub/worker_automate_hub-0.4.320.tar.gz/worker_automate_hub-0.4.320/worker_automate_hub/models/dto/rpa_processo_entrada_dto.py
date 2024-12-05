from datetime import datetime
from typing import List

from worker_automate_hub.models.dto.rpa_sistema_dto import RpaSistemaDTO
from pydantic import BaseModel, Field


class RpaProcessoEntradaDTO(BaseModel):
    datEntradaFila: datetime = Field(..., alias="datEntradaFila")
    configEntrada: dict = Field(..., alias="configEntrada")
    uuidProcesso: str = Field(..., alias="uuidProcesso")
    nomProcesso: str = Field(..., alias="nomProcesso")
    uuidFila: str = Field(..., alias="uuidFila")
    sistemas: List[RpaSistemaDTO] = Field(..., alias="sistemas")

    class Config:
        populate_by_name = True
