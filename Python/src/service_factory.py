# src/service_factory.py
from src.repository.monitoramento_repository import MonitoramentoRepository
from src.repository.aplicacao_monitoramento_repository import AplicacaoMonitoramentoRepository
from src.repository.cultura_produto_sensor_configuracao_repository import CulturaProdutoSensorConfiguracaoRepository
from src.services.monitoramento_service import MonitoramentoService
from src.services.aplicacao_service import AplicacaoService
from src.services.cultura_produto_sensor_configuracao_service import CulturaProdutoSensorConfiguracaoService
from src.services.cultura_produto_sensor_service import CulturaProdutoSensorService
from src.repository.cultura_produto_sensor_repository import CulturaProdutoSensorRepository


# Função para obter o serviço de Monitoramento
# Passando a dependência aqui
def get_monitoramento_service():
    monitoramento_repository = MonitoramentoRepository()
    aplicacao_service = get_aplicacao_service()  
    cultura_produto_sensor_configuracao_service = get_cultura_produto_sensor_configuracao_service() 
    cultura_produto_sensor_service = get_cultura_produto_sensor_service()
    return MonitoramentoService(monitoramento_repository, aplicacao_service, cultura_produto_sensor_configuracao_service, cultura_produto_sensor_service)

# Função para obter o serviço de Aplicação
def get_aplicacao_service():    
    repo = AplicacaoMonitoramentoRepository()
    return AplicacaoService(repo)

# Função para obter o serviço de CulturaProdutoSensorConfiguracao
def get_cultura_produto_sensor_configuracao_service():
    repo = CulturaProdutoSensorConfiguracaoRepository()
    return CulturaProdutoSensorConfiguracaoService(repo)

def get_cultura_produto_sensor_service():
    repo = CulturaProdutoSensorRepository()
    return CulturaProdutoSensorService(repo)



