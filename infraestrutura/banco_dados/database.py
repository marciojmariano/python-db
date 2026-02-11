import os
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

load_dotenv()

host=os.getenv("DB_HOST")
port=int(os.getenv("DB_PORT"))
user=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
database=os.getenv("DB_NAME")
url = f"postgresql://{user}:{password}@{host}:{port}/{database}"


engine = create_engine(
    url,  # URL de conexão com o banco (ex: mysql+pymysql://user:pass@host/db)
    pool_pre_ping=True,     # Valida a conexão antes de usar (evita erro com conexões "mortas" no pool)
    pool_size=10,           # Quantidade de conexões mantidas abertas no pool
    max_overflow=20,        # Conexões extras acima do pool_size que podem ser abertas temporariamente
)

SessionLocal = sessionmaker(
    autocommit=False,  # Não faz commit automático; você controla commit/rollback manualmente
    autoflush=False,   # Não faz flush automático; você controla quando enviar mudanças para o banco
    bind=engine        # Liga esta fábrica de sessões ao engine criado acima
)

Base = declarative_base()  # Classe base para seus modelos ORM (suas tabelas vão herdar dela)

def get_db() -> Generator[Session, None, None]:
    """Dependency para injetar sessão do banco nos endpoints."""
    db = SessionLocal()  # Cria uma sessão (unidade de trabalho) para conversar com o banco
    try:
        yield db          # Entrega a sessão para o endpoint (FastAPI injeta e usa durante a request)
    finally:
        db.close()        # Garante que a sessão/conexão seja fechada ao final (mesmo em caso de erro)