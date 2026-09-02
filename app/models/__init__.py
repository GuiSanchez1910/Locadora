"""Reexporta os modelos.

Importar este pacote na factory garante que todas as classes estejam
registradas no metadata antes de o Flask-Migrate comparar com o banco.
"""

from app.models.cliente import Cliente
from app.models.categoria import Categoria
from app.models.filme import Filme
from app.models.locacao import Locacao

__all__ = ["Cliente", "Categoria", "Filme", "Locacao"]

