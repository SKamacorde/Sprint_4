class Monitoramento:
    def __init__(self, cd_monitoramento, cd_cultura_produto_sensor, vlr_medido, dt_medicao, cd_usuario_inclusao, dt_inclusao): 
        self.cd_monitoramento = cd_monitoramento      
        self.cd_cultura_produto_sensor = cd_cultura_produto_sensor
        self.vlr_medido = vlr_medido
        self.dt_medicao = dt_medicao
        self.cd_usuario_inclusao = cd_usuario_inclusao
        self.dt_inclusao = dt_inclusao

    def __repr__(self):
        return f"<Monitoramento(cd_monitoramento={self.cd_monitoramento}, cd_cultura_produto_sensor='{self.cd_cultura_produto_sensor}', vlr_medido={self.vlr_medido}, dt_medicao={self.dt_medicao}, cd_usuario_inclusao={self.cd_usuario_inclusao},dt_inclusao={self.dt_inclusao})>"