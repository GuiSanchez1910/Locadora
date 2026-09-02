from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

class Cliente(db.Model):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key = True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique = True, nullable = False)
    email: Mapped[str] = mapped_column(String(150), unique = True, nullable = False)
    telefone: Mapped[str] = mapped_column(String(20), unique = True, nullable=False)

    def __repr__(self) -> str:
        return f"<Cliente {self.nome}>"
