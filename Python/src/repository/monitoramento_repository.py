from src.repository.base_repository import BaseRepository
from src.models.monitoramento import Monitoramento

class MonitoramentoRepository(BaseRepository):

    def buscar_monitoramento(self, cd_monitoramento):
        query = "SELECT * FROM TBL_MONITORAMENTO WHERE cd_monitoramento = %s"
        conn = self.get_connection()
        if conn is None:
            return None
        cursor = conn.cursor()
        cursor.execute(query, (cd_monitoramento,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return Monitoramento(*row) if row else None

    def inserir_monitoramento(self, monitoramento):
        insert_query = """
        INSERT INTO TBL_MONITORAMENTO 
        (cd_cultura_produto_sensor, vlr_medido, dt_medicao, cd_usuario_inclusao, dt_inclusao)
        VALUES (%s, %s, %s, %s, %s)
        """
        conn = self.get_connection()
        if conn is None:
            return None
        cursor = conn.cursor()
        try:
            cursor.execute(insert_query , (
                monitoramento.cd_cultura_produto_sensor,
                monitoramento.vlr_medido,
                monitoramento.dt_medicao,
                monitoramento.cd_usuario_inclusao,
                monitoramento.dt_inclusao
            ))
            conn.commit()
            # Busca o último ID inserido com SCOPE_IDENTITY()
            cursor.execute("SELECT SCOPE_IDENTITY()")
            result = cursor.fetchone()
            novo_id = result[0] if result else None
            return novo_id
        except Exception as e:
            print(f"Erro ao inserir monitoramento: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def listar_todos(self, cd_cultura_produto_sensor=None):
        query = "SELECT * FROM TBL_MONITORAMENTO"
        if cd_cultura_produto_sensor is not None:
            query += " WHERE cd_cultura_produto_sensor =  %s"

        conn = self.get_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        if cd_cultura_produto_sensor is not None:
            cursor.execute(query, (cd_cultura_produto_sensor,))
        else:
            cursor.execute(query)        
        monitoramentos = [Monitoramento(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return monitoramentos

    def atualizar_monitoramento(self, cd_monitoramento, vlr_medido):
        query = "UPDATE TBL_MONITORAMENTO SET vlr_medido = %s WHERE cd_monitoramento = %s"
        conn = self.get_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute(query, (vlr_medido, cd_monitoramento))
        conn.commit()
        cursor.close()
        conn.close()

    def deletar_monitoramento(self, cd_monitoramento):
        query = "DELETE FROM TBL_MONITORAMENTO WHERE cd_monitoramento = %s"
        conn = self.get_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute(query, (cd_monitoramento,))
        conn.commit()
        cursor.close()
        conn.close()
