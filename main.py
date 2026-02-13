import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importação da infraestrutura de banco de dados
from infraestrutura.banco_dados.database import engine, Base

# Importação das rotas de cada domínio
from api.rotas import (
    usuario_router,
    categoria_router,
    colaborador_router,
    ticket_router,
    ticket_historico_router
)

app = FastAPI(
    title="Sistema de Gestão de Tickets",
    description="API para gerenciamento de chamados internos e suporte técnico.",
    version="2.0.0"
)

# Inclusão das Rotas
app.include_router(usuario_router.router)
app.include_router(categoria_router.router)
app.include_router(colaborador_router.router)
app.include_router(ticket_router.router)
app.include_router(ticket_historico_router.router)

# Permite que eu rode o projeto dando um "python main.py"
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)