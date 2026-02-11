from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr, Field
from infraestrutura.banco_dados.modelos import CargoEnum


class ColaboradorCreateRequest(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100, description="Nome completo do colaborador")
    cargo: CargoEnum = Field(..., description="Nível de acesso: N1, N2, N3 ou Líder")
    cpf: str = Field(..., min_length=11, max_length=11, description="CPF apenas números")
    model_config = {
        "use_enum_values": True
    }

class ColaboradorResponse(BaseModel):
    id: uuid.UUID
    nome: str
    cargo: CargoEnum
    cpf: str
    created_at: datetime

    class Config:
        from_attributes = True

class ColaboradorUpdateRequest(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    cargo: Optional[CargoEnum] = None