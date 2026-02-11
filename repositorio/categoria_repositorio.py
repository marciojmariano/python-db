from sqlalchemy.orm import Session
from sqlalchemy import select
from infraestrutura.banco_dados.modelos import CategoriaEntidade
import uuid

class CategoriaRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        # Retorna todas as categorias ordenadas por nome
        return self.db.scalars(select(CategoriaEntidade).order_by(CategoriaEntidade.nome)).all()

    def buscar_por_id(self, id: uuid.UUID):
        return self.db.get(CategoriaEntidade, id)

    def criar(self, categoria_data: CategoriaEntidade):
        self.db.add(categoria_data)
        self.db.commit()
        self.db.refresh(categoria_data)
        return categoria_data

    def deletar(self, id: uuid.UUID):
        categoria = self.buscar_por_id(id)
        if categoria:
            self.db.delete(categoria)
            self.db.commit()
            return True
        return False