from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr, Field


class UsuarioCreateRequest(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=6, max_length=100)
    ativo: Optional[bool] = Field(default=True)

class UsuarioResponse(BaseModel):
    id: uuid.UUID
    nome: str
    email: EmailStr
    ativo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None