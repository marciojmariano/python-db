from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/calculadora")
def calculadora(numero1: int, numero2: int):
    soma = numero1 + numero2
    return {"resultado": soma}

# criar calculadora/expert com três parametros (query paramet) com operacao que vai ser um string e o n1 e o n2
# dentro da operação deverá somar ou subtrair
# response será um objeto contento os query parameters e resultado

# query param
@app.get("/calculadora/expert")
def calculadora_expert(operacao: str, n1: int, n2: int):
    if operacao == "soma" :
        resultado = n1 + n2
    elif operacao == "subtracao":
        resultado = n1 - n2
    else : 
        raise HTTPException(status_code=400, detail="Operacação invalida. Opções disponíveis: soma ou subtracao")
    return {"operacao": operacao, "numero1": n1, "numero2": n2, "resultado": resultado}

class AlunoCalcularMedia(BaseModel):
    nota1: float 
    nota2: float
    nota3: float


@app.post("/aluno/calcular-media")
def calcular_media(aluno_dados: AlunoCalcularMedia):
    media = (aluno_dados.nota1 + aluno_dados.nota2 + aluno_dados.nota3)/3
    return {"media": media}

# criar novo endpoint /aluno/status-aprovacao
# o body será enviado a média
# de acordo a média deverá retornar se o aluno está aprovado, reprovado ou em exame

class AlunoMedia(BaseModel):
    media: float

# body
@app.post("/aluno/status-aprovacao")
def analisar_aprovacao(aluno_media: AlunoMedia):
    print(type(aluno_media.media))
    if aluno_media.media >= 70:
        status_aprovacao = "aprovado"
    elif aluno_media.media < 70 and aluno_media.media >= 50:
        status_aprovacao = "exame"
    else: 
        status_aprovacao = "reprovado"
    return {"statusAprovacao": status_aprovacao}

alunos = {
    1: {
        "nome": "Márcio", "sobrenome": "Mariano"
    },
    2: {
        "nome": "Benjamin", "sobrenome": "José"
    },
}

# path param
@app.get("/aluno/{id}")
def retornar_dados_aluno(id: int):
    aluno_encontrado = alunos.get(id)
    if aluno_encontrado is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado com id")
    return aluno_encontrado

@app.get("/conversor/temperatura")
def converter_temperatura(temperatura_original: float, unidade_original: str, unidade_convertida: str):
    if unidade_original == "C" and unidade_convertida == "F":
        temperatura_convertida = (temperatura_original * 9/5) + 32
    elif unidade_original == "C" and unidade_convertida == "K":
        temperatura_convertida = (temperatura_original + 273.15)
    elif unidade_original == "F" and unidade_convertida == "C":
        temperatura_convertida = ((temperatura_original - 32) * 5/9)
    else:
        raise HTTPException(status_code=400, detail="Unidades de medida de temperatura inválidas. Opções disponíveis: C para Celsius, F para Fahrenheit e K para Kelvin")

    return {"temperatura_original": temperatura_original,
            "unidade_original": unidade_original,
            "temperatura_convertida": temperatura_convertida,
            "unidade_convertida": unidade_convertida}


class DadosImc(BaseModel):
    peso: float
    altura: float

@app.post("/saude/calcular-imc")
def calcular_imc(dados_imc: DadosImc):
    imc = dados_imc.peso / (dados_imc.altura * dados_imc.altura)

    if imc < 18.5:
        classificacao = "Abaixo do peso"
    elif imc >= 18.5 and imc <= 24.9:
        classificacao = "Peso normal"
    elif imc >= 25 and imc <= 29.9:
        classificacao = "Sobrepeso"
    else:
        classificacao = "Obesidade"
    
    return {
        "imc": round(imc, 2),  
        "classificacao": classificacao
    }

produtos = {
    1: {"nome": "Notebook", "preco": 3500.00, "estoque": 10},
    2: {"nome": "Mouse", "preco": 50.00, "estoque": 100},
    3: {"nome": "Teclado", "preco": 150.00, "estoque": 0}
}

@app.get("/produto/{id}")
def retornar_dados_produto(id: int):
    produto_pesquisado = produtos.get(id)
    if produto_pesquisado is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado com id")
    return produto_pesquisado

@app.get("/produto/{id}/disponibilidade")
def verificar_disponibilidade(id: int):
    produto_pesquisado = produtos.get(id)
    if produto_pesquisado is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    disponivel = produto_pesquisado["estoque"] > 0
    
    return {
        "disponibilidade": disponivel,
        "quantidade": produto_pesquisado["estoque"]
    }


