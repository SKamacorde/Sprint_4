from src.models.aplicacao_monitoramento import AplicacaoMonitoramento
from src.repository.base_repository import BaseRepository

class AplicacaoMonitoramentoRepository (BaseRepository):

    def obter_aplicacao(self, cd_aplicacao):
        # Exemplo com SQLAlchemy:
        query = "SELECT * FROM TBL_APLICACAO_MONITORAMENTO WHERE cd_aplicacao = %s"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (cd_aplicacao,))
            row = cursor.fetchone()
            return AplicacaoMonitoramento(*row) if row else None
    
    def inserir_aplicacao(self, aplicacaoMonitoramento):
        conn =  self.get_connection()       
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO TBL_APLICACAO_MONITORAMENTO (cd_monitoramento, vlr_medido, vlr_minimo,vlr_maximo, vlr_aplicado,cd_usuario_inclusao,dt_inclusao) VALUES(:1, :2, :3,:4,:5,:6,:7)"
            cursor.execute(sql, (aplicacaoMonitoramento.cd_monitoramento, aplicacaoMonitoramento.vlr_medido, aplicacaoMonitoramento.vlr_minimo, aplicacaoMonitoramento.vlr_maximo, 
                                 aplicacaoMonitoramento.vlr_aplicado, aplicacaoMonitoramento.cd_usuario_inclusao, aplicacaoMonitoramento.dt_inclusao))
            
            conn.commit()
            print("Aplicação inserida com sucesso.")
        except Exception as e:
            print(f"Erro ao inserir monitoramento: {e}")
            conn.rollback()
        finally:
            cursor.close()
    
    def listar_todos(self):
        conn =  self.get_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM TBL_APLICACAO_MONITORAMENTO"
            cursor.execute(query)
            monitoramentos = [AplicacaoMonitoramento(*row) for row in cursor.fetchall()]
            return monitoramentos
        finally:
            cursor.close()

    def deletar_aplicacao(self, cd_monitoramento):
        conn =  self.get_connection()  
        cursor = conn.cursor()
        try:
            query = "DELETE FROM TBL_APLICACAO_MONITORAMENTO  WHERE cd_monitoramento = :%s"
            cursor.execute(query, (cd_monitoramento,))
            conn.commit() 
        finally:
            cursor.close()