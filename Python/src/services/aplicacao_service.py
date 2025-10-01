from src.models.aplicacao_monitoramento import AplicacaoMonitoramento
from src.helpers.date_helper import DateHelper

class AplicacaoService:
    def __init__(self, aplicacao_monitoramento_repository):
       self.aplicacao_monitoramento_repository = aplicacao_monitoramento_repository

    def inserir_aplicacao(self, cd_monitoramento, vlr_medido, vlr_minimo, vlr_maximo, vlr_aplicado, cd_usuario_inclusao):
        # Aqui você pode adicionar qualquer validação/regra de negócio
        if not cd_monitoramento:
            raise ValueError("cd_monitoramento não pode ser nulo.")   
                     
        aplicacao_monitoramento = AplicacaoMonitoramento(cd_aplicacao=None, cd_monitoramento=cd_monitoramento,vlr_medido= vlr_medido,vlr_minimo= vlr_minimo,
                                                  vlr_maximo= vlr_maximo,vlr_aplicado= vlr_aplicado,cd_usuario_inclusao= cd_usuario_inclusao,dt_inclusao= DateHelper.now())
        
        self.aplicacao_monitoramento_repository.inserir_aplicacao(aplicacao_monitoramento)
        return aplicacao_monitoramento

    def obter_aplicacao(self, cd_aplicacao):
        aplicacao_monitoramento = self.aplicacao_monitoramento_repository.obter_aplicacao(cd_aplicacao)
        if not aplicacao_monitoramento:
            raise ValueError(f"Aplicação com ID {cd_aplicacao} não encontrado.")
        return aplicacao_monitoramento

    def listar_aplicacao(self):
        return self.aplicacao_monitoramento_repository.listar_todos()

    def deletar_aplicacao_monitoramento(self, cd_monitoramento):
        self.aplicacao_monitoramento_repository.deletar_aplicacao(cd_monitoramento)       