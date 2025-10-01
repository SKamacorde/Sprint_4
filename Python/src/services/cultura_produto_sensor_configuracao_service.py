from src.repository.cultura_produto_sensor_configuracao_repository import CulturaProdutoSensorConfiguracaoRepository

repo = CulturaProdutoSensorConfiguracaoRepository()
class CulturaProdutoSensorConfiguracaoService:
    def __init__(self, repo: CulturaProdutoSensorConfiguracaoRepository):
        self.repo = repo

    def obter_configuracao(self, cd_cultura_produto_sensor):
        configuracao = self.repo.obter_configuracao(cd_cultura_produto_sensor)
        if not configuracao:
            raise ValueError("Monitoramento não encontrado")
        return configuracao