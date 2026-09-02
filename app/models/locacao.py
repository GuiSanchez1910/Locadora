from datetime import datetime
from decimal import Decimal
from sqlalchemy import ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Locacao(db.Model):
    __tablename__ = "locacoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    filme_id: Mapped[int] = mapped_column(ForeignKey("filmes.id"), nullable=False)
    data_locacao: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    data_devolucao_prevista: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    data_devolucao: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ATIVA")

    cliente: Mapped["Cliente"] = relationship()
    filme: Mapped["Filme"] = relationship()

    def __repr__(self) -> str:
        return f"<Locacao {self.id}>"