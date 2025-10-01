from src.repository.base_repository import BaseRepository
from src.models.cultura_produto_sensor_configuracao import CulturaProdutoSensorConfiguracao

class CulturaProdutoSensorConfiguracaoRepository(BaseRepository):
   
    def obter_configuracao(self, cd_cultura_produto_sensor):
                 
        query = "SELECT * FROM TBL_CULTURA_PRODUTO_SENSOR_CONFIGURACAO WHERE cd_cultura_produto_sensor = %s"
        conn = self.get_connection()
        if conn is None:
            return None          
        cursor = conn.cursor()
        cursor.execute(query, (cd_cultura_produto_sensor,))
        row = cursor.fetchone()
        return CulturaProdutoSensorConfiguracao(*row) if row else None
    
    def listar_todos(self):
        conn =  self.get_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM TBL_CULTURA_PRODUTO_SENSOR_CONFIGURACAO"
            cursor.execute(query)
            configuracoes = [CulturaProdutoSensorConfiguracao(*row) for row in cursor.fetchall()]
            return configuracoes
        finally:
            cursor.close()