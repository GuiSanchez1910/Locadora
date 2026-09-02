from app.errors import RecursoNaoEncontrado, ReferenciaInvalida, RegraDeNegocio
from app.extensions import db
from app.models.categoria import Categoria
from app.models.filme import Filme
from app.models.locacao import Locacao

def listar() -> list[Locacao]:
    stmt = db.select(Locacao).order_by(Locacao.id)
    return list(db.session.scalars(stmt))