from sqlalchemy.orm import Session
from sqlalchemy import select
from infraestrutura.banco_dados.modelos import TicketEntidade, TicketHistoricoEntidade
import uuid

class TicketRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def listar_todos(self):
        # Usamos selectinload ou apenas confiamos no lazy load do SQLAlchemy 
        # para trazer os históricos e relacionamentos
        return self.db.scalars(select(TicketEntidade)).all()

    def buscar_por_id(self, id: uuid.UUID):
        return self.db.get(TicketEntidade, id)

    def criar(self, ticket: TicketEntidade, observacao_inicial: str):
        # 1. Adiciona o ticket
        self.db.add(ticket)
        self.db.flush() # Flush gera o ID do ticket sem commitar a transação ainda

        # 2. Cria o primeiro registro no histórico automaticamente
        historico_inicial = TicketHistoricoEntidade(
            id_ticket=ticket.id,
            status=ticket.status
        )
        self.db.add(historico_inicial)
        
        # 3. Commita ambos (Ticket + Histórico) como uma única operação
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def atualizar_status(self, ticket: TicketEntidade, novo_status, motivo: str):
        ticket.status = novo_status
        
        historico = TicketHistoricoEntidade(
            id_ticket=ticket.id,
            texto=motivo,
            status=novo_status
        )
        self.db.add(historico)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket