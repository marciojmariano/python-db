from sqlalchemy.orm import Session
from sqlalchemy import select
from infraestrutura.banco_dados.modelos import TicketHistoricoEntidade
import uuid

class TicketHistoricoRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def listar_por_ticket(self, id_ticket: uuid.UUID):
        # Busca todos os históricos de um ticket específico, do mais novo para o mais antigo
        return self.db.scalars(
            select(TicketHistoricoEntidade)
            .where(TicketHistoricoEntidade.id_ticket == id_ticket)
            .order_by(TicketHistoricoEntidade.created_at.desc())
        ).all()

    def criar(self, historico: TicketHistoricoEntidade):
        self.db.add(historico)
        self.db.commit()
        self.db.refresh(historico)
        return historico