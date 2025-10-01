class CulturaProdutoSensorService:
    def __init__(self, cultura_produto_sensor_repository):
        self.cultura_produto_sensor_repository = cultura_produto_sensor_repository

    def obter_por_id(self, cd_cultura_produto_sensor):
        cultura_produto_sensor = self.cultura_produto_sensor_repository.obter_configuracao(cd_cultura_produto_sensor)       
        return cultura_produto_sensor
    
    def listar_todos(self):
        lista =  self.cultura_produto_sensor_repository.listar_todos()  
        return lista
