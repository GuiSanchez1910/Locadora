from app.errors import RecursoNaoEncontrado, RegraDeNegocio
from app.extensions import db
from app.models.cliente import Cliente

def listar() -> list[Cliente]:
    stmt = db.select(Cliente).order_by(Cliente.nome)
    return list(db.session.scalars(stmt))

def obter(cliente_id: int) -> Cliente:
    cliente = db.session.get(Cliente, cliente_id)

    if cliente is None:
        raise RecursoNaoEncontrado(
            f"Cliente {cliente_id} não encontrado."
        )

    return cliente

def criar(dados: dict) -> Cliente:
    _garantir_cpf_disponivel(dados["cpf"])
    _garantir_email_disponivel(dados["email"])
    _garantir_telefone_disponivel(dados["telefone"])

    cliente = Cliente(**dados)

    db.session.add(cliente)
    db.session.commit()

    return cliente

def atualizar(cliente_id: int, dados: dict) -> Cliente:
    cliente = obter(cliente_id)

    if "cpf" in dados:
        _garantir_cpf_disponivel(dados["cpf"], cliente_id)

    if "email" in dados:
        _garantir_email_disponivel(dados["email"], cliente_id)

    if "telefone" in dados:
        _garantir_telefone_disponivel(dados["telefone"], cliente_id)

    for campo, valor in dados.items():
        setattr(cliente, campo, valor)

    db.session.commit()

    return cliente

def remover(cliente_id: int) -> None:
    cliente = obter(cliente_id)

    db.session.delete(cliente)
    db.session.commit()

def _garantir_cpf_disponivel(cpf: str, cliente_id: int | None = None) -> None:
    stmt = db.select(Cliente).where(Cliente.cpf == cpf)

    if cliente_id is not None:
        stmt = stmt.where(Cliente.id != cliente_id)

    if db.session.scalar(stmt) is not None:
        raise RegraDeNegocio("CPF já cadastrado.")

def _garantir_email_disponivel(
    email: str, cliente_id: int | None = None) -> None:
    stmt = db.select(Cliente).where(Cliente.email == email)

    if cliente_id is not None:
        stmt = stmt.where(Cliente.id != cliente_id)

    if db.session.scalar(stmt) is not None:
        raise RegraDeNegocio("E-mail já cadastrado.")

def _garantir_telefone_disponivel(telefone: str, cliente_id: int | None = None) -> None:
    stmt = db.select(Cliente).where(Cliente.telefone == telefone)

    if cliente_id is not None:
        stmt = stmt.where(Cliente.id != cliente_id)

    if db.session.scalar(stmt) is not None:
        raise RegraDeNegocio("Telefone já cadastrado.")