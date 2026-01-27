from datetime import date, datetime
import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from database import Base

from sqlalchemy import ForeignKey, String, Date, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column


class CategoriaCreateRequest(BaseModel):
    nome: str = Field(min_length=2, max_lenght=100)
    descricao: str = Field(min_length=2, max_lenght=100)


class CategoriaEntidade(Base):
    __tablename__ = "categorias"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime|None] = mapped_column(nullable=True, onupdate=func.now())

class CategoriaResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class UsuarioCreateRequest(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=6, max_length=100)
    ativo: Optional[bool] = Field(default=True)

class UsuarioEntidade(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(100), nullable=False)
    ativo: Mapped[bool] = mapped_column(nullable=False, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime|None] = mapped_column(nullable=True, onupdate=func.now())

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    ativo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class TicketCreateRequest(BaseModel):
    titulo: str = Field(min_length=5, max_length=150)
    descricao: str = Field(min_length=10)
    id_usuario: int = Field(description="ID do usuário que está abrindo o ticket")
    id_categoria: int = Field(description="ID da categoria do ticket")
    prioridade: Optional[str] = Field(default="media", pattern="^(baixa|media|alta)$")

class TicketResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: str
    prioridade: str
    id_usuario: int
    id_categoria: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class TicketEntidade(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), server_default=text("'aberto'"))
    prioridade: Mapped[str] = mapped_column(String(10), server_default=text("'media'"))

    # Chaves Estrangeiras (Relacionamentos)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categorias.id", ondelete="RESTRICT"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime|None] = mapped_column(nullable=True, onupdate=func.now())

class TicketUpdateRequest(BaseModel):
    titulo: str = Field(min_length=5, max_length=150)
    descricao: str = Field(min_length=10)
    id_categoria: int
    prioridade: str = Field(pattern="^(baixa|media|alta)$")
    status: str = Field(pattern="^(aberto|em_andamento|resolvido|cancelado)$")