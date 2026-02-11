from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from infraestrutura.banco_dados.database import get_db
from infraestrutura.banco_dados.modelos import ColaboradorEntidade
from repositorio.colaborador_repositorio import ColaboradorRepositorio
from api.schemas.colaborador_schemas import (
    ColaboradorResponse, 
    ColaboradorCreateRequest, 
    ColaboradorUpdateRequest
)

router = APIRouter(prefix="/colaboradores", tags=["Colaboradores"])

@router.get("/", response_model=List[ColaboradorResponse])
def listar(db: Session = Depends(get_db)):
    repo = ColaboradorRepositorio(db)
    return repo.listar()

@router.post("/", response_model=ColaboradorResponse, status_code=status.HTTP_201_CREATED)
def criar(request: ColaboradorCreateRequest, db: Session = Depends(get_db)):
    repo = ColaboradorRepositorio(db)
    novo_colaborador = ColaboradorEntidade(
        nome=request.nome,
        cargo=request.cargo,
        cpf=request.cpf
    )
    return repo.criar(novo_colaborador)

@router.get("/{id}", response_model=ColaboradorResponse)
def obter(id: uuid.UUID, db: Session = Depends(get_db)):
    repo = ColaboradorRepositorio(db)
    colaborador = repo.buscar_por_id(id)
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return colaborador

@router.put("/{id}", response_model=ColaboradorResponse)
def atualizar(id: uuid.UUID, request: ColaboradorUpdateRequest, db: Session = Depends(get_db)):
    repo = ColaboradorRepositorio(db)
    colaborador_db = repo.buscar_por_id(id)
    
    if not colaborador_db:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    
    # Atualiza apenas os campos enviados
    dados_atualizados = request.model_dump(exclude_unset=True)
    for chave, valor in dados_atualizados.items():
        setattr(colaborador_db, chave, valor)
    
    return repo.atualizar(colaborador_db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(id: uuid.UUID, db: Session = Depends(get_db)):
    repo = ColaboradorRepositorio(db)
    if not repo.deletar(id):
        raise HTTPException(status_code=404, detail="Colaborador não encontrado para exclusão")
    return None