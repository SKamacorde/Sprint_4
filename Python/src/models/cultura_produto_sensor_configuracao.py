class CulturaProdutoSensorConfiguracao:
    def __init__(self, cd_cultura_produto_sensor_configuracao , cd_cultura_produto_sensor,  vlr_minimo,vlr_maximo, cd_usuario_inclusao, dt_inclusao):
        self.cd_cultura_produto_sensor_configuracao = cd_cultura_produto_sensor_configuracao
        self.cd_cultura_produto_sensor = cd_cultura_produto_sensor
        self.vlr_minimo = vlr_minimo
        self.vlr_maximo = vlr_maximo
        self.cd_usuario_inclusao = cd_usuario_inclusao
        self.dt_inclusao = dt_inclusao

    def __repr__(self):
        return f"<CulturaProdutoSensorConfiguracao(cd_cultura_produto_sensor={self.cd_cultura_produto_sensor}, vlr_minimo='{self.vlr_minimo}', vlr_maximo={self.vlr_maximo})>"