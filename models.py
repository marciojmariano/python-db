from datetime import date, datetime
import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class TurmaCreateRequest(BaseModel):
    nome: str = Field(min_length=2, max_lenght=100)
    sigla: str = Field(min_length=2, max_lenght=3)

class TurmaResponse(BaseModel):
    nome: str
    sigla: str
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class ProfessorCreateRequest(BaseModel):
    # cpf: str = Field(min_length=11, max_lenght=14)
    nome: str = Field(min_length=2, max_lenght=100)
    sobrenome: str = Field(min_length=2, max_lenght=100)
    email: EmailStr
    data_nascimento: date

    # @field_validator('cpf')
    # @classmethod
    # def preparar_cpf(cls, v: str) -> str:
    #     # 1. Remove qualquer caractere que não seja número (pontos, traços, espaços)
    #     cpf_limpo = re.sub(r'\D', '', v)
        
    #     # 2. Verifica se sobraram exatamente 11 números
    #     if len(cpf_limpo) != 11:
    #         raise ValueError('O CPF deve ter 11 dígitos numéricos')
            
    #     return cpf_limpo

class ProfessorResponse(BaseModel):
    id: int
    # cpf: str
    nome: str
    sobrenome: str
    data_nascimento: date
    created_at: datetime
    updated_at: Optional[datetime] = None