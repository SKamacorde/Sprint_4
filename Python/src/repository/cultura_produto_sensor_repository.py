from src.repository.base_repository import BaseRepository
from src.models.cultura_produto_sensor import CulturaProdutoSensor

class CulturaProdutoSensorRepository(BaseRepository):
   
    def obter_por_id(self, cd_cultura_produto_sensor):
        # Exemplo com SQLAlchemy:        
        query = "SELECT * FROM TBL_CULTURA_PRODUTO_SENSOR WHERE cd_cultura_produto_sensor = %s"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (cd_cultura_produto_sensor,))
            row = cursor.fetchone()
            return CulturaProdutoSensor(*row) if row else None
    
    def listar_todos(self):
        conn =  self.get_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM TBL_CULTURA_PRODUTO_SENSOR"
            cursor.execute(query)
            configuracoes = [CulturaProdutoSensor(*row) for row in cursor.fetchall()]
            return configuracoes
        finally:
            cursor.close()