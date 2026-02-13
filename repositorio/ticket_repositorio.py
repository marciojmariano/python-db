from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from api.schemas.ticket_schemas import TicketCloseRequest, TicketDoneRequest, TicketReopenRequest, TicketStartRequest
from infraestrutura.banco_dados.database import get_db
from infraestrutura.banco_dados.modelos import TicketEntidade, TicketHistoricoEntidade
import uuid

from infraestrutura.banco_dados.modelos.enums import TicketStatusEnum

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

    def iniciar_ticket(self, ticket: TicketEntidade, payload: TicketStartRequest):
        ticket.status = TicketStatusEnum.em_andamento.value
        ticket.id_responsavel = payload.responsavel_id
        ticket.tempo_estimado = payload.tempo_estimado
        ticket.ob = payload.observacoes_iniciais
        ticket.updated_at = func.now()

        novo_historico = TicketHistoricoEntidade(
            id_ticket=ticket.id,
            status=TicketStatusEnum.em_andamento.value,
        )
        
        self.db.add(novo_historico)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def encerrar_ticket(self, ticket: TicketEntidade, payload: TicketDoneRequest):
        # 1. Atualiza o ticket para 'resolvido'
        ticket.status = TicketStatusEnum.resolvido
        ticket.solucao_aplicada = payload.solucao_aplicada
        ticket.observacoes_internas = payload.observacoes_internas
        ticket.updated_at = func.now()

        # 2. Registra no histórico
        novo_historico = TicketHistoricoEntidade(
            id_ticket=ticket.id,
            status=TicketStatusEnum.resolvido,
        )
        
        self.db.add(novo_historico)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
    
    def fechar_ticket(self, ticket: TicketEntidade, payload: TicketCloseRequest):
        # 1. Finaliza os dados de avaliação
        ticket.status = TicketStatusEnum.concluido
        ticket.avaliacao = payload.avaliacao
        ticket.comentario_avaliacao = payload.comentario_avaliacao
        ticket.updated_at = func.now()

        # 2. Registra o histórico de conclusão
        novo_historico = TicketHistoricoEntidade(
            id_ticket=ticket.id,
            status=TicketStatusEnum.concluido,
        )
        
        self.db.add(novo_historico)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
    
    def reabrir_ticket(self, ticket: TicketEntidade, payload: TicketReopenRequest):
        # 1. Volta o status para Em Andamento
        ticket.status = TicketStatusEnum.em_andamento
        ticket.reabertura_motivo = payload.motivo_reabertura
        ticket.reabertura_detalhes = payload.motivo_detalhes
        ticket.updated_at = func.now()

        # 2. Registra o histórico da reabertura
        novo_historico = TicketHistoricoEntidade(
            id_ticket=ticket.id,
            status=TicketStatusEnum.em_andamento,
        )
        
        self.db.add(novo_historico)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket