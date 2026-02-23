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

# Adicionar ao models.py
class TicketComentarioEntidade(Base):
    __tablename__ = "ticket_comentarios"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    id_ticket: Mapped[int] = mapped_column(ForeignKey('tickets.id'), nullable=False)
    id_colaborador: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), nullable=False)
    comentario: Mapped[str] = mapped_column(String(500), nullable=False)
    data: Mapped[datetime] = mapped_column(server_default=func.now())