from src.repository.base_repository import BaseRepository
from src.models.produto import Produto

class ProdutoRepository(BaseRepository):
    
    def listar_todos(self):
        conn =  self.get_connection()  
        cursor = conn.cursor()
        try:
            sql = "SELECT * FROM TBL_PRODUTO"
            cursor.execute(sql)
            produtos = [Produto(*row) for row in cursor.fetchall()]
            return produtos
        finally:
            cursor.close()