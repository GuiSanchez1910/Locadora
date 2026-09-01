from app.errors import RecursoNaoEncontrado, ReferenciaInvalida, RegraDeNegocio
from app.extensions import db
from app.models.categoria import Categoria
from app.models.filme import Filme


def listar() -> list[Filme]:
    stmt = db.select(Filme).order_by(Filme.titulo)
    return list(db.session.scalars(stmt))


def obter(filme_id: int) -> Filme:
    filme = db.session.get(Filme, filme_id)
    if filme is None:
        raise RecursoNaoEncontrado(f"Filme {filme_id} não encontrado.")
    return filme


def criar(dados: dict) -> Filme:
    _garantir_categoria_existe(dados["categoria_id"])

    filme = Filme(**dados)
    _sincronizar_disponibilidade(filme)
    db.session.add(filme)
    db.session.commit()
    return filme


def atualizar(filme_id: int, dados: dict) -> Filme:
    filme = obter(filme_id)

    if "categoria_id" in dados:
        _garantir_categoria_existe(dados["categoria_id"])

    for campo, valor in dados.items():
        setattr(filme, campo, valor)

    _sincronizar_disponibilidade(filme)
    db.session.commit()
    return filme


def remover(filme_id: int) -> None:
    filme = obter(filme_id)
    db.session.delete(filme)
    db.session.commit()


def alugar(filme_id: int) -> Filme:
    filme = obter(filme_id)
    if not filme.disponivel:
        raise RegraDeNegocio("Filme indisponível para locação.")

    filme.estoque -= 1
    _sincronizar_disponibilidade(filme)
    db.session.commit()
    return filme


def devolver(filme_id: int) -> Filme:
    filme = obter(filme_id)
    filme.estoque += 1
    _sincronizar_disponibilidade(filme)
    db.session.commit()
    return filme


def _garantir_categoria_existe(categoria_id: int) -> None:
    if db.session.get(Categoria, categoria_id) is None:
        raise ReferenciaInvalida(f"Categoria {categoria_id} não encontrada.")


def _sincronizar_disponibilidade(filme: Filme) -> None:
    filme.disponivel = filme.estoque > 0
