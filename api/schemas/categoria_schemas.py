from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field

class CategoriaCreateRequest(BaseModel):
    nome: str = Field(min_length=2, max_lenght=100)
    descricao: str = Field(min_length=2, max_lenght=100)

class CategoriaResponse(BaseModel):
    id: uuid.UUID
    nome: str
    descricao: str
    created_at: datetime
    updated_at: Optional[datetime] = None

