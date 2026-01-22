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

from models import AlunoCreateRequest, AlunoEntidade, AlunoResponse, ProfessorCreateRequest, ProfessorEntidade, ProfessorResponse, TurmaCreateRequest, TurmaEntidade, TurmaResponse

# Base.metadata.create_all(bind=engine) Não é uma boa pratica

app = FastAPI()


class ApiTag(str, Enum):
    ALUNOS = "Alunos"
    PROFESSORES = "Professores"
    TURMAS = "Turmas"


# def get_connection():
#     host = os.getenv("DB_HOST")
#     porta = int(os.getenv("DB_PORT"))
#     usuario = os.getenv("DB_USER")
#     senha = os.getenv("DB_PASSWORD")
#     db = os.getenv("DB_NAME")

#     return pymysql.connect(
#         host=host,
#         port=porta,
#         user=usuario,
#         password=senha,
#         database=db,
#         autocommit=False,
#         cursorclass=DictCursor,
#         charset="utf8mb4"
#     )

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

  
@app.post("/turmas", status_code=status.HTTP_201_CREATED, response_model = TurmaResponse, tags=[ApiTag.TURMAS])
def criar_turma(payload: TurmaCreateRequest, db: Session=Depends(get_db)):
    professor = db.get(ProfessorEntidade, payload.id_professor)    
    if professor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Professor não encontrado id: {payload.id_professor}")
    turma = TurmaEntidade(
        nome = payload.nome,
        sigla = payload.sigla,
        id_professor = payload.id_professor
    )
    db.add(turma)
    db.commit()
    db.refresh(turma)
    return turma

# @app.get("/turmas")
@app.get("/turmas", response_model=list[TurmaResponse], tags=[ApiTag.TURMAS])
def listar_turmas(db:Session = Depends(get_db)):
    turmas = db.scalars(select(TurmaEntidade).order_by(TurmaEntidade.nome.asc())).all()
    return turmas

# GET /turmas/{id} (id é um query param) buscar a turma por id, caso não exista retornar 404
@app.get("/turmas/{id}", response_model = TurmaResponse, tags=[ApiTag.TURMAS])
def consultar_turma(id: int, db:Session = Depends(get_db)):
    turma = db.get(TurmaEntidade, id)
    if turma is None:
        raise HTTPException(status_code=404, detail="Truma não encontrada")
    return turma

# DELETE /turmas/{id} (id é um query param) apagar turma, caso não exista retornar 404
@app.delete("/turmas/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=[ApiTag.TURMAS])
def consultar_turma(id: int, db: Session=Depends(get_db)):
    turma = db.get(TurmaEntidade, id)
    if turma is None:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    db.delete(turma)
    db.commit()
    
# PUT /turmas/{id} (id é um query param) body é {"nome": "nome da turma", "sigla": "sigla da turma"} alterar turma, caso não exista retornar 404
@app.put("/turmas/{id}", response_model = TurmaResponse, tags=[ApiTag.TURMAS])
def atualizar_turma(id: int, payload: TurmaCreateRequest, db: Session=Depends(get_db)):
    turma = db.get(TurmaEntidade, id)
    if turma is None:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    professor = db.get(ProfessorEntidade, payload.id_professor)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado")     
    turma.nome = payload.nome
    turma.sigla = payload.sigla
    turma.id_professor = payload.id_professor
    db.commit()
    db.refresh(turma)
    return turma

# Códigos de retornos:
# 200 OK = Sucesso genérico
# 201 Created = Algo foi criado (melhor pra POST!)
# 204 No Content = Sucesso sem retorno
# 400 Bad Request = Erro do cliente
# 404 Not Found = Não encontrado
# 500 Internal Server Error = Erro do servidor

# CRUD PROFESSOR 
@app.post("/professores", status_code=status.HTTP_201_CREATED, response_model = ProfessorResponse, tags=[ApiTag.PROFESSORES])
def criar_professor(payload: ProfessorCreateRequest, db: Session =Depends(get_db)):
    professor = ProfessorEntidade(
        nome = payload.nome,
        sobrenome = payload.sobrenome,
        email = payload.email,
        data_nascimento = payload.data_nascimento
    )
    db.add(professor)
    db.commit()
    db.refresh(professor)
    return professor

@app.get("/professores", response_model=list[ProfessorResponse], tags=[ApiTag.PROFESSORES])
def listar_professores(db:Session = Depends(get_db)):
    professores = db.scalars(select(ProfessorEntidade).order_by(ProfessorEntidade.nome.asc())).all()
    return professores

@app.get("/professores/{id}", response_model = ProfessorResponse, tags=[ApiTag.PROFESSORES])
def consultar_professor(id: int, db:Session=Depends(get_db)):
    professor_consultado = db.get(ProfessorEntidade, id)
    if professor_consultado is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return professor_consultado

@app.delete("/professores/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=[ApiTag.PROFESSORES])
def apagar_professor(id: int, db:Session=Depends(get_db)):
    professor_a_deletar = db.get(ProfessorEntidade, id)
    if professor_a_deletar is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    db.delete(professor_a_deletar)
    db.commit()

@app.put("/professores/{id}", response_model = ProfessorResponse, tags=[ApiTag.PROFESSORES])
def atualizar_professor(id: int, payload: ProfessorCreateRequest, db:Session=Depends(get_db)):
    professor = db.get(ProfessorEntidade, id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    professor.nome = payload.nome
    professor.sobrenome = payload.sobrenome
    professor.email = payload.email
    professor.data_nascimento = payload.data_nascimento

    db.commit()    
    db.refresh(professor)   
    return professor
    
# CRUD ALUNO 
@app.post("/alunos", status_code=status.HTTP_201_CREATED, response_model = AlunoResponse, tags=[ApiTag.ALUNOS])
def criar_aluno(payload: AlunoCreateRequest, db: Session=Depends(get_db)):
    aluno = AlunoEntidade(
        nome = payload.nome,
        sobrenome = payload.sobrenome,
        email = payload.email,
        data_nascimento = payload.data_nascimento
    )
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno

@app.get("/alunos", response_model=list[AlunoResponse], tags=[ApiTag.ALUNOS])
def listar_alunos(db:Session = Depends(get_db)):
    alunos = db.scalars(select(AlunoEntidade).order_by(AlunoEntidade.nome.asc())).all()
    return alunos

@app.get("/alunos/{id}", response_model = AlunoResponse, tags=[ApiTag.ALUNOS])
def consultar_aluno(id: int, db:Session = Depends(get_db)):
    aluno = db.get(AlunoEntidade, id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@app.delete("/alunos/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=[ApiTag.ALUNOS])
def deletar_aluno(id: int, db:Session = Depends(get_db)):
    aluno = db.get(AlunoEntidade, id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(aluno)
    db.commit()

@app.put("/alunos/{id}", response_model = AlunoResponse, tags=[ApiTag.ALUNOS])
def atualizar_aluno(id: int, payload: AlunoCreateRequest, db:Session = Depends(get_db)):
    aluno = db.get(AlunoEntidade, id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    aluno.nome = payload.nome,
    aluno.sobrenome = payload.sobrenome
    aluno.email = payload.email,
    aluno.data_nascimento = payload.data_nascimento
    db.commit()
    db.refresh(aluno)
    return aluno