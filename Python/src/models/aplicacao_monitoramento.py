class AplicacaoMonitoramento:
    def __init__(self, cd_aplicacao, cd_monitoramento, vlr_medido,vlr_minimo,vlr_maximo, vlr_aplicado, cd_usuario_inclusao, dt_inclusao):
        self.cd_aplicacao = cd_aplicacao
        self.cd_monitoramento = cd_monitoramento
        self.vlr_medido = vlr_medido
        self.vlr_minimo = vlr_minimo
        self.vlr_maximo = vlr_maximo
        self.vlr_aplicado = vlr_aplicado
        self.cd_usuario_inclusao = cd_usuario_inclusao
        self.dt_inclusao = dt_inclusao

    def __repr__(self):
        return f"<AplicacaoMonitoramento(cd_aplicacao={self.cd_aplicacao}, cd_monitoramento={self.cd_monitoramento}, vlr_medido='{self.vlr_medido}', vlr_minimo='{self.vlr_minimo}',vlr_maximo='{self.vlr_maximo}',vlr_aplicado={self.vlr_aplicado})>"