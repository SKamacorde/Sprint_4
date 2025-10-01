from models.produto import Produto
from repository.produto_repository import ProdutoRepository
class ProdutoService:
    def __init__(self, repo: ProdutoRepository):
        self.repo = repo

    def listar_monitoramentos(self):
        return self.repo.listar_todos(self)