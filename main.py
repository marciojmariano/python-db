import os
from typing import Union

from sqlalchemy import select
from database import Base, engine, get_db
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from pydantic import BaseModel
from pymysql.cursors import DictCursor
from enum import Enum

from models import CategoriaCreateRequest, CategoriaEntidade, CategoriaResponse, TicketCreateRequest, TicketEntidade, TicketResponse, TicketUpdateRequest, UsuarioCreateRequest, UsuarioEntidade, UsuarioResponse


# Base.metadata.create_all(bind=engine) Não é uma boa pratica

app = FastAPI()


class ApiTag(str, Enum):
    USUARIOS = "Usuarios"
    CATEGORIAS = "Categorias"
    TICKETS = "Tickets"


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursor_factory=RealDictCursor
    )

@app.get("/")
def read_root():
    return {"Hello": "World"}

  
@app.post("/categorias", status_code=status.HTTP_201_CREATED, response_model = CategoriaResponse, tags=[ApiTag.TURMAS])
def criar_categoria(payload: CategoriaCreateRequest, db: Session=Depends(get_db)):
    categoria = CategoriaEntidade(
        nome = payload.nome,
        descricao = payload.descricao
    )
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

# @app.get("/categorias")
@app.get("/categorias", response_model=list[CategoriaResponse], tags=[ApiTag.CATEGORIAS])
def listar_categorias(db:Session = Depends(get_db)):
    categorias = db.scalars(select(CategoriaEntidade).order_by(CategoriaEntidade.nome.asc())).all()
    return categorias

# GET /categorias/{id} (id é um query param) buscar a categoria por id, caso não exista retornar 404
@app.get("/categorias/{id}", response_model = CategoriaResponse, tags=[ApiTag.CATEGORIAS])
def consultar_categoria(id: int, db:Session = Depends(get_db)):
    categoria = db.get(CategoriaEntidade, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

# DELETE /categorias/{id} (id é um query param) apagar categoria, caso não exista retornar 404
@app.delete("/categorias/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=[ApiTag.CATEGORIAS])
def deletar_categoria(id: int, db: Session=Depends(get_db)):
    categoria = db.get(CategoriaEntidade, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db.delete(categoria)
    db.commit()
    return

# PUT /categorias/{id} (id é um query param) body é {"nome": "nome da categorias", "descricao": "descricao da categoria"} alterar categorias, caso não exista retornar 404
@app.put("/categorias/{id}", response_model = CategoriaResponse, tags=[ApiTag.CATEGORIAS])
def atualizar_categoria(id: int, payload: CategoriaCreateRequest, db: Session=Depends(get_db)):
    categoria = db.get(CategoriaEntidade, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    categoria.nome = payload.nome
    categoria.descricao = payload.descricao
    db.commit()
    db.refresh(categoria)
    return categoria

# Códigos de retornos:
# 200 OK = Sucesso genérico
# 201 Created = Algo foi criado (melhor pra POST!)
# 204 No Content = Sucesso sem retorno
# 400 Bad Request = Erro do cliente
# 404 Not Found = Não encontrado
# 500 Internal Server Error = Erro do servidor

# CRUD USUARIO 

 
@app.post("/usuarios", status_code=status.HTTP_201_CREATED, response_model = UsuarioResponse, tags=[ApiTag.USUARIOS])
def criar_usuario(payload: UsuarioCreateRequest, db: Session=Depends(get_db)):
    usuario = UsuarioEntidade(
        nome = payload.nome,
        email = payload.email,
        senha = payload.senha,
        ativo = payload.ativo
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

# @app.get("/usuarios")
@app.get("/usuarios", response_model=list[UsuarioResponse], tags=[ApiTag.usuarios])
def listar_usuarios(db:Session = Depends(get_db)):
    usuarios = db.scalars(select(UsuarioEntidade).order_by(UsuarioEntidade.nome.asc())).all()
    return usuarios

# GET /usuarios/{id} (id é um query param) buscar a usuario por id, caso não exista retornar 404
@app.get("/usuarios/{id}", response_model = UsuarioResponse, tags=[ApiTag.usuarios])
def consultar_usuario(id: int, db:Session = Depends(get_db)):
    usuario = db.get(UsuarioEntidade, id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="usuario não encontrada")
    return usuario

# DELETE /usuarios/{id} (id é um query param) apagar usuario, caso não exista retornar 404
@app.delete("/usuarios/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=[ApiTag.usuarios])
def deletar_usuario(id: int, db: Session=Depends(get_db)):
    usuario = db.get(UsuarioEntidade, id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="usuario não encontrada")
    db.delete(usuario)
    db.commit()
    return

# PUT /usuarios/{id} (id é um query param) body é {"nome": "nome da usuarios", "email": "email da usuario"} alterar usuarios, caso não exista retornar 404
@app.put("/usuarios/{id}", response_model = UsuarioResponse, tags=[ApiTag.usuarios])
def atualizar_usuario(id: int, payload: UsuarioCreateRequest, db: Session=Depends(get_db)):
    usuario = db.get(UsuarioEntidade, id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="usuario não encontrada")
    usuario.nome = payload.nome
    usuario.senha = payload.senha
    usuario.ativo = payload.ativo
    db.commit()
    db.refresh(usuario)
    return usuario
    
# CRUD ticket 
@app.post("/tickets", status_code=status.HTTP_201_CREATED, response_model=TicketResponse, tags=[ApiTag.TICKETS])
def criar_ticket(payload: TicketCreateRequest, db: Session = Depends(get_db)):

    usuario = db.get(UsuarioEntidade, payload.id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuário ID {payload.id_usuario} não encontrado")
    
    categoria = db.get(CategoriaEntidade, payload.id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail=f"Categoria ID {payload.id_categoria} não encontrada")

    ticket = TicketEntidade(
        titulo=payload.titulo,
        descricao=payload.descricao,
        prioridade=payload.prioridade,
        id_usuario=payload.id_usuario,
        id_categoria=payload.id_categoria
    )
    
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

# GET /tickets - Listar todos os tickets
@app.get("/tickets", response_model=list[TicketResponse], tags=[ApiTag.TICKETS])
def listar_tickets(db: Session = Depends(get_db)):
    return db.scalars(select(TicketEntidade).order_by(TicketEntidade.created_at.desc())).all()

# GET /tickets/{id} (id é um query param) buscar a tickets por id, caso não exista retornar 404
@app.get("/tickets/{id}", response_model=TicketResponse, tags=[ApiTag.TICKETS])
def consultar_ticket(id: int, db: Session = Depends(get_db)):
    ticket = db.get(TicketEntidade, id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    return ticket

# PUT /tickets/{id} (id é um query param) body é {"titulo": "titulo usuarios", "desri": "email da usuario"} alterar usuarios, caso não exista retornar 404
@app.put("/tickets/{id}", response_model=TicketResponse, tags=[ApiTag.TICKETS])
def atualizar_ticket(id: int, payload: TicketUpdateRequest, db: Session = Depends(get_db)):
    ticket = db.get(TicketEntidade, id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    categoria = db.get(CategoriaEntidade, payload.id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria informada não existe")

    ticket.titulo = payload.titulo
    ticket.descricao = payload.descricao
    ticket.id_categoria = payload.id_categoria
    ticket.prioridade = payload.prioridade
    ticket.status = payload.status 
    
    db.commit()
    db.refresh(ticket)
    return ticket

# DELETE /tickets/{id} (id é um query param) apagar tickets, caso não exista retornar 404
@app.delete("/tickets/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=[ApiTag.TICKETS])
def deletar_ticket(id: int, db: Session = Depends(get_db)):
    ticket = db.get(TicketEntidade, id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    db.delete(ticket)
    db.commit()
    return