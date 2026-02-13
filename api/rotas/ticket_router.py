from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from infraestrutura.banco_dados.database import get_db
from infraestrutura.banco_dados.modelos import TicketEntidade
from infraestrutura.banco_dados.modelos.enums import TicketStatusEnum
from repositorio.ticket_repositorio import TicketRepositorio
from api.schemas.ticket_schemas import TicketCloseRequest, TicketDoneRequest, TicketReopenRequest, TicketResponse, TicketCreateRequest, TicketStartRequest

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.get("/", response_model=List[TicketResponse])
def listar_tickets(db: Session = Depends(get_db)):
    repo = TicketRepositorio(db)
    return repo.listar_todos()

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def criar_ticket(request: TicketCreateRequest, db: Session = Depends(get_db)):
    repo = TicketRepositorio(db)
    
    # Preparamos a entidade
    novo_ticket = TicketEntidade(
        titulo=request.titulo,
        descricao=request.descricao,
        prioridade=request.prioridade,
        id_usuario=request.id_usuario,
        id_categoria=request.id_categoria,
        status="aberto"
    )
    
    # O repositório cuida da criação do ticket e do histórico inicial
    return repo.criar(novo_ticket, observacao_inicial=request.descricao)

@router.get("/{id}", response_model=TicketResponse)
def obter_ticket(id: uuid.UUID, db: Session = Depends(get_db)):
    repo = TicketRepositorio(db)
    ticket = repo.buscar_por_id(id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    return ticket

@router.put("/{id}/start", response_model=TicketResponse)
def iniciar_ticket(id: uuid.UUID, payload: TicketStartRequest, db: Session = Depends(get_db)):
    repo = TicketRepositorio(db)
    
    # Busca o ticket pelo ID
    ticket = repo.buscar_por_id(id)
    
    # Validações de regra de negócio
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    if ticket.status != TicketStatusEnum.aberto.value:
        raise HTTPException(
            status_code=400, 
            detail=f"Não é possível iniciar um ticket com status {ticket.status.value}"
        )

    # Chama o repositório para executar a ação
    return repo.iniciar_ticket(ticket, payload)

@router.put("/{id}/done", response_model=TicketResponse)
def encerrar_ticket(id: uuid.UUID, payload: TicketDoneRequest, db: Session = Depends(get_db)):
    repo = TicketRepositorio(db)
    ticket = repo.buscar_por_id(id)
    
    # 1. Verifica existência
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    # 2. Valida regra de estado (Só encerra se estiver em andamento)
    if ticket.status != TicketStatusEnum.em_andamento.value:
        raise HTTPException(
            status_code=400, 
            detail="Para encerrar um ticket, ele precisa estar em andamento!"
        )

    # 3. Executa a ação
    return repo.encerrar_ticket(ticket, payload)

@router.put("/{id}/close", response_model=TicketResponse)
def fechar_ticket(id: uuid.UUID, payload: TicketCloseRequest, db: Session = Depends(get_db)):
    repo = TicketRepositorio(db)
    ticket = repo.buscar_por_id(id)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")

    # Regra de Negócio: Só fecha se o técnico já tiver dado o 'done' (Resolvido)
    if ticket.status != TicketStatusEnum.resolvido.value:
        raise HTTPException(
            status_code=400, 
            detail="O ticket precisa estar com status 'Resolvido' para ser concluído."
        )

    return repo.fechar_ticket(ticket, payload)

@router.put("/{id}/reopen", response_model=TicketResponse)
def reabrir_ticket(id: uuid.UUID, payload: TicketReopenRequest, db: Session = Depends(get_db)):
    repo = TicketRepositorio(db)
    ticket = repo.buscar_por_id(id)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")

    # Regra: Só reabre se o técnico deu o 'done' (Resolvido), mas o cliente não gostou
    if ticket.status != TicketStatusEnum.resolvido.value:
        raise HTTPException(
            status_code=400, 
            detail=f"Não é possível reabrir. O status atual é {ticket.status.value}, mas deveria ser 'Resolvido'."
        )

    return repo.reabrir_ticket(ticket, payload)