from datetime import datetime, timezone
from app.errors import RecursoNaoEncontrado, ReferenciaInvalida, RegraDeNegocio
from app.extensions import db
from app.models.cliente import Cliente
from app.models.filme import Filme
from app.models.locacao import Locacao

def listar() -> list[Locacao]:
    stmt = db.select(Locacao).order_by(Locacao.data_locacao.desc())
    return list(db.session.scalars(stmt))


def obter(locacao_id: int) -> Locacao:
    locacao = db.session.get(Locacao, locacao_id)
    if locacao is None:
        raise RecursoNaoEncontrado(f"Locação {locacao_id} não encontrada.")
    return locacao

def criar(dados: dict) -> Locacao:
    _garantir_cliente_existe(dados["cliente_id"])
    filme = _garantir_filme_existe(dados["filme_id"])

    if not filme.disponivel:
        raise RegraDeNegocio("Filme indisponível para locação.")

    dados.setdefault("data_locacao", datetime.now(timezone.utc))
    dados.setdefault("status", True)

    locacao = Locacao(**dados)

    filme.estoque -= 1
    _sincronizar_disponibilidade(filme)

    db.session.add(locacao)
    db.session.commit()
    return locacao


def atualizar(locacao_id: int, dados: dict) -> Locacao:
    locacao = obter(locacao_id)

    if "filme_id" in dados and dados["filme_id"] != locacao.filme_id:
        raise RegraDeNegocio("Não é possível trocar o filme de uma locação existente.")

    if "cliente_id" in dados:
        _garantir_cliente_existe(dados["cliente_id"])

    for campo, valor in dados.items():
        setattr(locacao, campo, valor)

    db.session.commit()
    return locacao


def remover(locacao_id: int) -> None:
    locacao = obter(locacao_id)
    db.session.delete(locacao)
    db.session.commit()


def devolver(locacao_id: int) -> Locacao:
    locacao = obter(locacao_id)

    if not locacao.status:
        raise RegraDeNegocio("Locação já foi devolvida.")

    filme = db.session.get(Filme, locacao.filme_id)
    if filme is None:
        raise RecursoNaoEncontrado(f"Filme {locacao.filme_id} não encontrado.")

    locacao.status = False
    locacao.data_devolucao = datetime.now(timezone.utc)

    filme.estoque += 1
    _sincronizar_disponibilidade(filme)

    db.session.commit()
    return locacao


def _garantir_cliente_existe(cliente_id: int) -> None:
    if db.session.get(Cliente, cliente_id) is None:
        raise ReferenciaInvalida(f"Cliente {cliente_id} não encontrado.")


def _garantir_filme_existe(filme_id: int) -> Filme:
    filme = db.session.get(Filme, filme_id)
    if filme is None:
        raise ReferenciaInvalida(f"Filme {filme_id} não encontrado.")
    return filme


def _sincronizar_disponibilidade(filme: Filme) -> None:
    filme.disponivel = filme.estoque > 0