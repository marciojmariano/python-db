from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from infraestrutura.banco_dados.database import get_db
from infraestrutura.banco_dados.modelos import TicketEntidade
from repositorio.ticket_repositorio import TicketRepositorio
from api.schemas.ticket_schemas import TicketResponse, TicketCreateRequest

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