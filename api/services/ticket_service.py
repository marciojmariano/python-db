from sqlalchemy.orm import Session
from api.schemas.ticket_schemas import TicketCreateRequest
from infraestrutura.banco_dados.modelos import TicketEntidade
from repositorio.ticket_repositorio import TicketRepositorio

class TicketService:
    @staticmethod
    def criar_novo_ticket(db: Session, request: TicketCreateRequest) -> TicketEntidade:
        repo = TicketRepositorio(db)
        
        # A regra de negócio (status padrão) fica no Service
        novo_ticket = TicketEntidade(
            titulo=request.titulo,
            descricao=request.descricao,
            prioridade=request.prioridade,
            id_usuario=request.id_usuario,
            id_categoria=request.id_categoria,
            status="aberto"
        )
        
        # O Service delega a persistência para o Repositório
        return repo.criar(novo_ticket, observacao_inicial=request.descricao)