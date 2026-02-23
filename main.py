import logging
from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config import settings # Importante para os requisitos 5b e 5c

# Importação das rotas de cada domínio
from api.rotas import (
    usuario_router,
    categoria_router,
    colaborador_router,
    ticket_router,
    ticket_historico_router
)

# 1. Configuração de Logs
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# 2. Instância ÚNICA do App (Consolida Requisito 5c e Metadados)
app = FastAPI(
    title="Sistema de Gestão de Tickets",
    description="API para gerenciamento de chamados internos e suporte técnico.",
    version="2.0.0",
    # Aplica a lógica de segurança
    docs_url="/docs" if settings.is_swagger_enabled() else None,
    redoc_url="/redoc" if settings.is_swagger_enabled() else None
)

# 3. Adicionar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Inclusão das Rotas
app.include_router(usuario_router.router)
app.include_router(categoria_router.router)
app.include_router(colaborador_router.router)
app.include_router(ticket_router.router)
app.include_router(ticket_historico_router.router)


# Permite que eu rode o projeto dando um "python main.py"
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)