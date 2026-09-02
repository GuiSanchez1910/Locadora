from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

class Locacao(db.Model):
    __tablename__ = "locacacoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    filme_id: Mapped[int] = mapped_column(ForeignKey("filmes.id"), nullable=False)
    data_locacao: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    data_devolucao_prevista: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    data_devolucao: Mapped[datetime | None] = mapped_column(DateTime, nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0.0)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<Locacao {self.id}>"