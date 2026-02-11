from sqlalchemy.orm import Session
from sqlalchemy import select
from infraestrutura.banco_dados.modelos import UsuarioEntidade
import uuid

class UsuarioRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.scalars(select(UsuarioEntidade)).all()

    def buscar_por_id(self, id: uuid.UUID):
        return self.db.get(UsuarioEntidade, id)

    def buscar_por_email(self, email: str):
        # Útil para validações de duplicidade ou login futuro
        return self.db.scalar(select(UsuarioEntidade).where(UsuarioEntidade.email == email))

    def criar(self, usuario: UsuarioEntidade):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario