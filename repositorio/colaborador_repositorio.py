from sqlalchemy.orm import Session
from sqlalchemy import select
from infraestrutura.banco_dados.modelos import ColaboradorEntidade
import uuid

class ColaboradorRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.scalars(select(ColaboradorEntidade)).all()

    def buscar_por_id(self, id: uuid.UUID):
        return self.db.get(ColaboradorEntidade, id)

    def criar(self, colaborador: ColaboradorEntidade):
        self.db.add(colaborador)
        self.db.commit()
        self.db.refresh(colaborador)
        return colaborador

    def atualizar(self, colaborador_db: ColaboradorEntidade):
        self.db.commit()
        self.db.refresh(colaborador_db)
        return colaborador_db

    def deletar(self, id: uuid.UUID) -> bool:
        colaborador = self.buscar_por_id(id)
        if colaborador:
            self.db.delete(colaborador)
            self.db.commit()
            return True
        return False