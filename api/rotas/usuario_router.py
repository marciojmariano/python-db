from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from infraestrutura.banco_dados.database import get_db
from infraestrutura.banco_dados.modelos import UsuarioEntidade
from repositorio.usuario_repositorio import UsuarioRepositorio
from api.schemas.usuario_schemas import UsuarioResponse, UsuarioCreateRequest

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    repo = UsuarioRepositorio(db)
    return repo.listar()

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(request: UsuarioCreateRequest, db: Session = Depends(get_db)):
    repo = UsuarioRepositorio(db)
    
    # Validação simples: verificar se e-mail já existe
    if repo.buscar_por_email(request.email):
        raise HTTPException(
            status_code=400, 
            detail="Já existe um usuário cadastrado com este e-mail."
        )
    
    novo_usuario = UsuarioEntidade(
        nome=request.nome,
        email=request.email,
        senha=request.senha, # Em produção, aqui você usaria um hash!
        ativo=True
    )
    
    return repo.criar(novo_usuario)

@router.get("/{id}", response_model=UsuarioResponse)
def obter_usuario(id: uuid.UUID, db: Session = Depends(get_db)):
    repo = UsuarioRepositorio(db)
    usuario = repo.buscar_por_id(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario