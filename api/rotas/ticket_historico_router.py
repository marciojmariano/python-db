from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from infraestrutura.banco_dados.database import get_db
from infraestrutura.banco_dados.modelos import TicketHistoricoEntidade
from repositorio.ticket_historico_repositorio import TicketHistoricoRepositorio
from api.schemas.ticket_historico_schemas import TicketHistoricoResponse, TicketHistoricoCreateRequest

router = APIRouter(prefix="/historicos", tags=["Históricos"])

@router.get("/ticket/{id_ticket}", response_model=List[TicketHistoricoResponse])
def listar_historico_do_ticket(id_ticket: uuid.UUID, db: Session = Depends(get_db)):
    repo = TicketHistoricoRepositorio(db)
    return repo.listar_por_ticket(id_ticket)

@router.post("/", response_model=TicketHistoricoResponse)
def adicionar_interacao(request: TicketHistoricoCreateRequest, db: Session = Depends(get_db)):
    repo = TicketHistoricoRepositorio(db)
    
    nova_interacao = TicketHistoricoEntidade(
        id_ticket=request.id_ticket,
        texto=request.texto,
        status=request.status
    )
    
    return repo.criar(nova_interacao)