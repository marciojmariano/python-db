import enum
from typing import List, Optional
import uuid
from uuid6 import uuid7
from datetime import datetime
from sqlalchemy import UUID, Enum, ForeignKey, String, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infraestrutura.banco_dados.database import Base
from .enums import TicketStatusEnum, TicketPrioridadeEnum
from .colaborador_modelo import ColaboradorEntidade
from .ticket_historico_modelo import TicketHistoricoEntidade
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .colaborador_modelo import ColaboradorEntidade
    from .ticket_historico_modelo import TicketHistoricoEntidade

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
    observacoes_iniciais: Mapped[str | None] = mapped_column(Text, nullable=True)
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
