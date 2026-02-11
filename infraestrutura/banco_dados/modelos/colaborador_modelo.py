from typing import List
import uuid
from sqlalchemy import Enum
from uuid6 import uuid7
from datetime import datetime
from infraestrutura.banco_dados.database import Base
from .enums import CargoEnum
from sqlalchemy import UUID, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

# Incluído para resolver o problema de Erro de Importação Circular
#Colaborador tenta importar o Ticket, e o Ticket (através do __init__.py) tenta importar o Colaborador ao mesmo tempo. O Python entra em loop e trava.

if TYPE_CHECKING:
    from .ticket_modelo import TicketEntidade

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
