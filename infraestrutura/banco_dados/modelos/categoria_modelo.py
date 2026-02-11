import uuid
from uuid6 import uuid7
from datetime import datetime
from infraestrutura.banco_dados.database import Base
from sqlalchemy import UUID, String, func
from sqlalchemy.orm import Mapped, mapped_column

class CategoriaEntidade(Base):
    __tablename__ = "categorias"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime|None] = mapped_column(nullable=True, onupdate=func.now())