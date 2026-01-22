from datetime import date, datetime
import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

from database import Base

from sqlalchemy import ForeignKey, String, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TurmaCreateRequest(BaseModel):
    nome: str = Field(min_length=2, max_lenght=100)
    sigla: str = Field(min_length=2, max_lenght=3)
    id_professor: int = Field()

class TurmaEntidade(Base):
    __tablename__ = "turmas"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    sigla: Mapped[str] = mapped_column(String(3), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime|None] = mapped_column(nullable=True, onupdate=func.now())
    id_professor: Mapped[int] = mapped_column(ForeignKey('professores.id'), nullable=False)
    professor: Mapped['ProfessorEntidade'] = relationship('ProfessorEntidade', back_populates='turmas')

class TurmaResponse(BaseModel):
    nome: str
    sigla: str
    id: int
    id_professor: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class ProfessorEntidade(Base):
    __tablename__ = "professores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    sobrenome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime|None] = mapped_column(nullable=True, onupdate=func.now())
    turmas: Mapped[list['TurmaEntidade']] = relationship('TurmaEntidade', back_populates='professor')


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

class AlunoCreateRequest(BaseModel):
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

class AlunoEntidade(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    sobrenome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime|None] = mapped_column(nullable=True, onupdate=func.now())

class AlunoResponse(BaseModel):
    id: int
    # cpf: str
    nome: str
    sobrenome: str
    email: EmailStr
    data_nascimento: date
    created_at: datetime
    updated_at: Optional[datetime] = None