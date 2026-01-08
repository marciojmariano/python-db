import os
from typing import Union

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import pymysql
from pymysql.cursors import DictCursor

from models import AlunoCreateRequest, AlunoResponse, ProfessorCreateRequest, ProfessorResponse, TurmaCreateRequest, TurmaResponse

load_dotenv()

app = FastAPI()

def obter_conexao():
    host = os.getenv("DB_HOST")
    porta = int(os.getenv("DB_PORT"))
    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASSWORD")
    db = os.getenv("DB_NAME")

    return pymysql.connect(
        host=host,
        port=porta,
        user=usuario,
        password=senha,
        database=db,
        autocommit=False,
        cursorclass=DictCursor,
        charset="utf8mb4"
    )

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/turmas")
@app.get("/turmas", response_model=list[TurmaResponse])
def listar_turmas():
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute("select * from turmas")
        turmas = cursor.fetchall()
        cursor.close()
        return turmas
    finally:
        conexao.close()
    
@app.post("/turmas", status_code=status.HTTP_201_CREATED, response_model = TurmaResponse)
def criar_turma(payload: TurmaCreateRequest):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        sql = "insert into turmas (nome, sigla) values (%s, %s)"
        dados = (payload.nome, payload.sigla)
        cursor.execute(sql, dados)
        turma_id = cursor.lastrowid
        cursor.execute("select * from turmas where id = %s", (turma_id,))
        turma = cursor.fetchone()
        conexao.commit()
        cursor.close()
        return turma
    
    finally:
        conexao.close()

# GET /turmas/{id} (id é um query param) buscar a turma por id, caso não exista retornar 404
@app.get("/turmas/{id}", response_model = TurmaResponse)
def consultar_turma(id: int):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute("select * from turmas where id = %s", (id,))
        turma_consultada = cursor.fetchone()
        cursor.close()
        if turma_consultada is None:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        return turma_consultada
    finally:
        conexao.close()

# DELETE /turmas/{id} (id é um query param) apagar turma, caso não exista retornar 404
@app.delete("/turmas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def consultar_turma(id: int):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute("select * from turmas where id = %s", (id,))
        turma_a_deletar = cursor.fetchone()
        if turma_a_deletar is None:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        sql = "delete from turmas turmas where id = %s"
        cursor.execute(sql, id)
        conexao.commit()
        cursor.close()
        return
    finally:
        conexao.close()

# PUT /turmas/{id} (id é um query param) body é {"nome": "nome da turma", "sigla": "sigla da turma"} alterar turma, caso não exista retornar 404
@app.put("/turmas/{id}", response_model = TurmaResponse)
def atualizar_turma(id: int, payload: TurmaCreateRequest):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()

        cursor.execute("select * from turmas where id = %s", (id,))
        turma= cursor.fetchone()
        if turma is None:
            raise HTTPException(status_code=404, detail="Turma não encontrada")
        sql = "update turmas SET nome = %s, sigla = %s WHERE id = %s"
        dados = (payload.nome, payload.sigla, id)
        cursor.execute(sql, dados)
        conexao.commit()
       
        cursor.execute("select * from turmas where id = %s", (id,))
        turma= cursor.fetchone()
        cursor.close()
        return turma
    
    finally:
        conexao.close()

# Códigos de retornos:
# 200 OK = Sucesso genérico
# 201 Created = Algo foi criado (melhor pra POST!)
# 204 No Content = Sucesso sem retorno
# 400 Bad Request = Erro do cliente
# 404 Not Found = Não encontrado
# 500 Internal Server Error = Erro do servidor

# CRUD PROFESSOR 
@app.post("/professores", status_code=status.HTTP_201_CREATED, response_model = ProfessorResponse)
def criar_professor(payload: ProfessorCreateRequest):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        sql = "insert into professores (nome, sobrenome, email, data_nascimento) values (%s, %s, %s, %s)"
        dados = (payload.nome, payload.sobrenome, payload.email, payload.data_nascimento)
        cursor.execute(sql, dados)
        professor_id = cursor.lastrowid
        cursor.execute("select * from professores where id = %s", (professor_id,))
        professor = cursor.fetchone()
        conexao.commit()
        cursor.close()
        return professor
    
    finally:
        conexao.close()

@app.get("/professores", response_model=list[ProfessorResponse])
def listar_professores():
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute("select * from professores")
        professores = cursor.fetchall()
        cursor.close()
        return professores
    finally:
        conexao.close()

@app.get("/professores/{id}", response_model = ProfessorResponse)
def consultar_professor(id: int):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute("select * from professores where id = %s", (id,))
        professor_consultado = cursor.fetchone()
        cursor.close()
        if professor_consultado is None:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        return professor_consultado
    finally:
        conexao.close()

@app.delete("/professores/{id}", status_code=status.HTTP_204_NO_CONTENT)
def consultar_professor(id: int):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute("select * from professores where id = %s", (id,))
        professor_a_deletar = cursor.fetchone()
        if professor_a_deletar is None:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        sql = "delete from professores where id = %s"
        cursor.execute(sql, id)
        conexao.commit()
        cursor.close()
        return
    finally:
        conexao.close()

@app.put("/professores/{id}", response_model = ProfessorResponse)
def atualizar_professor(id: int, payload: ProfessorCreateRequest):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()

        cursor.execute("select * from professores where id = %s", (id,))
        professor= cursor.fetchone()
        if professor is None:
            raise HTTPException(status_code=404, detail="Professor não encontrado")
        sql = "update professores SET nome = %s, sobrenome = %s, email = %s, data_nascimento = %s WHERE id = %s"
        dados = (payload.nome, payload.sobrenome, payload.email, payload.data_nascimento, id)
        cursor.execute(sql, dados)
        conexao.commit()
       
        cursor.execute("select * from professores where id = %s", (id,))
        professor= cursor.fetchone()
        cursor.close()
        return professor
    
    finally:
        conexao.close()

# CRUD ALUNO 
@app.post("/alunos", status_code=status.HTTP_201_CREATED, response_model = AlunoResponse)
def criar_aluno(payload: AlunoCreateRequest):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        sql = "insert into alunos (nome, sobrenome, email, data_nascimento) values (%s, %s, %s, %s)"
        dados = (payload.nome, payload.sobrenome, payload.email, payload.data_nascimento)
        cursor.execute(sql, dados)
        aluno_id = cursor.lastrowid
        cursor.execute("select * from alunos where id = %s", (aluno_id,))
        aluno = cursor.fetchone()
        conexao.commit()
        cursor.close()
        return aluno
    
    finally:
        conexao.close()

@app.get("/alunos", response_model=list[AlunoResponse])
def listar_alunos():
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute("select * from alunos")
        alunos = cursor.fetchall()
        cursor.close()
        return alunos
    finally:
        conexao.close()

@app.get("/alunos/{id}", response_model = AlunoResponse)
def consultar_aluno(id: int):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute("select * from alunos where id = %s", (id,))
        aluno_consultado = cursor.fetchone()
        cursor.close()
        if aluno_consultado is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        return aluno_consultado
    finally:
        conexao.close()

@app.delete("/alunos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def consultar_turma(id: int):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute("select * from alunos where id = %s", (id,))
        aluno_a_deletar = cursor.fetchone()
        if aluno_a_deletar is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        sql = "delete from alunos where id = %s"
        cursor.execute(sql, id)
        conexao.commit()
        cursor.close()
        return
    finally:
        conexao.close()

@app.put("/alunos/{id}", response_model = AlunoResponse)
def atualizar_aluno(id: int, payload: AlunoCreateRequest):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()

        cursor.execute("select * from alunos where id = %s", (id,))
        aluno = cursor.fetchone()
        if aluno is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        sql = "update alunos SET nome = %s, sobrenome = %s, email = %s, data_nascimento = %s WHERE id = %s"
        dados = (payload.nome, payload.sobrenome, payload.email, payload.data_nascimento, id)
        cursor.execute(sql, dados)
        conexao.commit()
       
        cursor.execute("select * from alunos where id = %s", (id,))
        aluno = cursor.fetchone()
        cursor.close()
        return aluno
    
    finally:
        conexao.close()