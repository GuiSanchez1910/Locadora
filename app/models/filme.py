from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Filme(db.Model):
    __tablename__ = "filmes"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ano: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duracao: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estoque: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    disponivel: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"), nullable=False)

    categoria: Mapped["Categoria"] = relationship()

    def __repr__(self) -> str:
        return f"<Filme {self.titulo}>"
