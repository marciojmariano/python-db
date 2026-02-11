from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from infraestrutura.banco_dados.database import get_db
from infraestrutura.banco_dados.modelos import CategoriaEntidade
from repositorio.categoria_repositorio import CategoriaRepositorio
from api.schemas.categoria_schemas import CategoriaResponse, CategoriaCreateRequest

# Definimos o prefixo para não precisar repetir "/categorias" em cada rota
router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    repo = CategoriaRepositorio(db)
    return repo.listar()

@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(request: CategoriaCreateRequest, db: Session = Depends(get_db)):
    repo = CategoriaRepositorio(db)
    # Transformamos o Schema em Entidade
    nova_categoria = CategoriaEntidade(
        nome=request.nome,
        descricao=request.descricao
    )
    return repo.criar(nova_categoria)

@router.get("/{id}", response_model=CategoriaResponse)
def obter_categoria(id: uuid.UUID, db: Session = Depends(get_db)):
    repo = CategoriaRepositorio(db)
    categoria = repo.buscar_por_id(id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria