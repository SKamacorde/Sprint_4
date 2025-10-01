class CulturaProdutoSensor:
    def __init__(self, cd_cultura_produto_sensor , cd_cultura,  cd_produto_sensor, cd_usuario_inclusao, dt_inclusao):
        self.cd_cultura_produto_sensor = cd_cultura_produto_sensor        
        self.cd_cultura = cd_cultura
        self.cd_produto_sensor = cd_produto_sensor
        self.cd_usuario_inclusao = cd_usuario_inclusao
        self.dt_inclusao = dt_inclusao

    def __repr__(self):
        return f"<CulturaProdutoSensor(cd_cultura_produto_sensor={self.cd_cultura_produto_sensor}, cd_cultura='{self.cd_cultura}', cd_produto_sensor={self.cd_produto_sensor},cd_usuario_inclusao={self.cd_usuario_inclusao},dt_inclusao={self.dt_inclusao})>"