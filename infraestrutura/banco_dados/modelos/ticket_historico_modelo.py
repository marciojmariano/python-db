from typing import List, TYPE_CHECKING
import uuid
import enum
from uuid6 import uuid7
from datetime import datetime
from infraestrutura.banco_dados.database import Base
from .enums import TicketStatusEnum 
from sqlalchemy import UUID, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .ticket_modelo import TicketEntidade

class TicketHistoricoEntidade(Base):
    __tablename__ = "ticket_historicos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    id_ticket: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[TicketStatusEnum] = mapped_column(Enum(TicketStatusEnum), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    ticket: Mapped["TicketEntidade"] = relationship(back_populates="historicos")
