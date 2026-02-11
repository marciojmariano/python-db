import uuid
from uuid6 import uuid7
import enum
from datetime import date, datetime
import re
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from database import Base
from sqlalchemy import UUID, String, ForeignKey, Text, func, text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class CategoriaCreateRequest(BaseModel):
    nome: str = Field(min_length=2, max_lenght=100)
    descricao: str = Field(min_length=2, max_lenght=100)


class CategoriaEntidade(Base):
    __tablename__ = "categorias"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime|None] = mapped_column(nullable=True, onupdate=func.now())

class CategoriaResponse(BaseModel):
    id: uuid.UUID
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

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(100), nullable=False)
    ativo: Mapped[bool] = mapped_column(nullable=False, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime|None] = mapped_column(nullable=True, onupdate=func.now())

class UsuarioResponse(BaseModel):
    id: uuid.UUID
    nome: str
    email: EmailStr
    ativo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class CargoEnum(enum.Enum):
    n1 = "n1"
    n2 = "n2"
    n3 = "n3"
    lider = "lider"

class ColaboradorEntidade(Base):
    __tablename__ = "colaboradores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Usando o Enum do SQLAlchemy para os cargos
    cargo: Mapped[CargoEnum] = mapped_column(
        Enum(CargoEnum), 
        nullable=False
    )
    
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relacionamento: Um colaborador pode ter vários tickets sob sua responsabilidade
    tickets: Mapped[List["TicketEntidade"]] = relationship(back_populates="responsavel")

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


# Definindo o Enum para o Python entender os status do banco
class TicketStatusEnum(enum.Enum):
    aberto = "aberto"
    em_andamento = "em_andamento"
    resolvido = "resolvido"
    concluido = "concluido"
    excluido = "excluido"

class TicketPrioridadeEnum(enum.Enum):
    baixa = "baixa"
    importante = "importante"
    urgente = "urgente"

class TicketEntidade(Base):
    __tablename__ = "tickets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Atualizado para usar o Enum nativo que criamos no SQL
    status: Mapped[TicketStatusEnum] = mapped_column(
        Enum(TicketStatusEnum), 
        server_default=text("'aberto'"),
        nullable=False
    )
    prioridade: Mapped[TicketPrioridadeEnum] = mapped_column(
        Enum(TicketPrioridadeEnum),
        nullable=False
        )

    # Novos campos de Workflow
    tempo_estimado: Mapped[int | None] = mapped_column(nullable=True)
    obersavoces_iniciais: Mapped[str | None] = mapped_column(Text, nullable=True)
    solucao_aplicada: Mapped[str | None] = mapped_column(Text, nullable=True)
    observacoes_internas: Mapped[str | None] = mapped_column(Text, nullable=True)
    reabertura_motivo: Mapped[str | None] = mapped_column(Text, nullable=True)
    reabertura_detalhes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Campos de Avaliação
    avaliacao: Mapped[int | None] = mapped_column(nullable=True)
    comentario_avaliacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    comentario_confirmacao_usuario: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Chaves Estrangeiras
    id_usuario: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    id_categoria: Mapped[uuid.UUID] = mapped_column(ForeignKey("categorias.id", ondelete="RESTRICT"), nullable=False)
    id_responsavel: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("colaboradores.id", ondelete="SET NULL"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(nullable=True, onupdate=func.now())

    # Relacionamento com o Responsável
    responsavel: Mapped[Optional["ColaboradorEntidade"]] = relationship(back_populates="tickets")

    # Relacionamento com o Histórico
    historicos: Mapped[list["TicketHistoricoEntidade"]] = relationship(back_populates="ticket", cascade="all, delete-orphan")

class TicketHistoricoEntidade(Base):
    __tablename__ = "ticket_historicos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    id_ticket: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[TicketStatusEnum] = mapped_column(Enum(TicketStatusEnum), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    ticket: Mapped["TicketEntidade"] = relationship(back_populates="historicos")

class TicketHistoricoResponse(BaseModel):
    id: uuid.UUID
    status: TicketStatusEnum
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

class TicketResponse(BaseModel):
    id: uuid.UUID
    titulo: str
    status: TicketStatusEnum
    prioridade: TicketPrioridadeEnum
    id_usuario: uuid.UUID
    id_responsavel: Optional[uuid.UUID] = None
    created_at: datetime
    historicos: List[TicketHistoricoResponse] = []
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

class TicketCreateRequest(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=150)
    descricao: str = Field(..., min_length=10)
    id_usuario: uuid.UUID = Field(..., description="ID do usuário que está abrindo o ticket")
    id_categoria: uuid.UUID = Field(..., description="ID da categoria do ticket")
    prioridade: TicketPrioridadeEnum = Field(..., description="Prioridades: baixa, importante e urgente")
    model_config = {"use_enum_values": True}
    


# PUT /tickets/{id}/start
class TicketStartRequest(BaseModel):
    responsavel_id: int
    tempo_estimado: int = Field(..., ge=1, le=7) # Min 1 dia, Max 7 dias
    obersavoces_iniciais: str = Field(..., min_length=30)

# PUT /tickets/{id}/done
class TicketDoneRequest(BaseModel):
    solucao_aplicada: str = Field(..., min_length=100)
    observacoes_internas: Optional[str] = None

# PUT /tickets/{id}/reopen
class TicketReopenRequest(BaseModel):
    motivo_reabertura: str = Field(..., min_length=1)
    motivo_detalhes: str = Field(..., min_length=1)

# PUT /tickets/{id}/close
class TicketCloseRequest(BaseModel):
    avaliacao: int = Field(..., ge=1, le=5)
    comentario_avaliacao: Optional[str] = None
    comentario_confirmacao_usuario: str = Field(..., min_length=30)



