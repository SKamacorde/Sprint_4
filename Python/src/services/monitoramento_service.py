# src/services/monitoramento_service.py
from src.models.monitoramento import Monitoramento
from src.helpers.date_helper import DateHelper
import pandas as pd
class MonitoramentoService:
    def __init__(self, monitoramento_repository, aplicacao_service, cultura_produto_sensor_configuracao_service, cultura_produto_sensor_service):
        self.monitoramento_repository = monitoramento_repository
        self.aplicacao_service = aplicacao_service
        self.cultura_produto_sensor_configuracao_service = cultura_produto_sensor_configuracao_service
        self.cultura_produto_sensor_service = cultura_produto_sensor_service

    def inserir_monitoramento(self, cd_cultura_produto_sensor, vlr_medido, dt_medicao, cd_usuario_inclusao):
        # Validações
        if not cd_cultura_produto_sensor:
            raise ValueError("cd_cultura_produto_sensor não pode ser vazia.")
        if not vlr_medido:
            raise ValueError("vlr_medido não pode ser vazia.")
        if not dt_medicao:
            raise ValueError("dt_medicao não pode ser vazia.")
        if not cd_usuario_inclusao:
            raise ValueError("cd_usuario_inclusao não pode ser vazia.")
        
        # Inserir dados
        monitoramento = Monitoramento(cd_monitoramento=None, cd_cultura_produto_sensor= cd_cultura_produto_sensor, vlr_medido =vlr_medido, dt_medicao = DateHelper.parse_datetime_auto(dt_medicao), 
                                      cd_usuario_inclusao =cd_usuario_inclusao ,dt_inclusao= DateHelper.now())
                
        cd_monitoramento = self.monitoramento_repository.inserir_monitoramento(monitoramento)    

        # Regras de negócio       
        configuracao = self.cultura_produto_sensor_configuracao_service.obter_configuracao(cd_cultura_produto_sensor)
        if vlr_medido < configuracao.vlr_minimo or vlr_medido > configuracao.vlr_maximo:
            print("\n💧 ALERTA DE UMIDADE 💧")
            print(f"Dispositivo {cd_cultura_produto_sensor} registrou {vlr_medido}% "
              f"(fora da faixa {configuracao.vlr_minimo}-{configuracao.vlr_maximo}%)\n")         
            print(f"[EMAIL] Para: suporte@empresa.com")
            print(f"Assunto: ALERTA {cd_cultura_produto_sensor} - Umidade crítica")
            print(f"Mensagem: Umidade fora da faixa aceitável: {vlr_medido}%\n") 

        return monitoramento       

    def buscar_monitoramento(self, cd_monitoramento):
        monitoramento = self.monitoramento_repository.buscar_monitoramento(cd_monitoramento)      
        return monitoramento

    def listar_monitoramentos(self, cd_cultura_produto_sensor=None):        
        monitoramentos = self.monitoramento_repository.listar_todos(cd_cultura_produto_sensor=cd_cultura_produto_sensor)
        return monitoramentos
    
    def atualizar_monitoramento(self, cd_monitoramento, vlr_medido):
        self.monitoramento_repository.atualizar_monitoramento(cd_monitoramento, vlr_medido) 

    def deletar_monitoramento(self, cd_monitoramento):
        self.aplicacao_service.deletar_aplicacao_monitoramento(cd_monitoramento)
        self.monitoramento_repository.deletar_monitoramento(cd_monitoramento) 

    def importacao_arquivo(self):    
        # Lendo o CSV com o parser de data e tratando valores inválidos
        try:
            df = pd.read_csv("src/documents/monitoramento.csv", 
                             header=None,  # Indica que não há cabeçalho
                             names=["CD_CULTURA_PRODUTO_SENSOR", "VLR_MEDIDO", "DT_MEDICAO", "CD_USUARIO_INCLUSAO"], # Definindo os nomes das colunas
                             converters={"DT_MEDICAO": DateHelper.parse_date})
            
            #Remove espaços extras nos nomes das colunas
            df.columns.str.strip()            
            # Usando apply para processar cada linha
            df.apply(self.processar_linha, axis=1)

        except FileNotFoundError:
            print("Arquivo CSV não encontrado.")
        except pd.errors.ParserError:
            print("Erro ao ler o arquivo CSV.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def processar_linha(self, row):
        # Inserir os dados de monitoramento
        self.inserir_monitoramento(int(row['CD_CULTURA_PRODUTO_SENSOR']), float(row['VLR_MEDIDO']),  row['DT_MEDICAO'],int(row['CD_USUARIO_INCLUSAO'])) 

    @staticmethod
    def formartar_retorno(monitoramento):
        print(f'{'cd_monitoramento'.ljust(25)} | {'cd_cultura_produto_sensor'.ljust(25)} | {'vlr_medido'.ljust(25)} | {'dt_medicao'.ljust(25)} | {'cd_usuario_inclusao'.ljust(25)} | {'dt_inclusao'.ljust(25)}')
        cd_monitoramento_str = str(monitoramento.cd_cultura_produto_sensor )      
        cd_cultura_produto_sensor_str = str(monitoramento.cd_cultura_produto_sensor )        
        vlr_medido_str = str(monitoramento.vlr_medido )  
        dt_medicao_str = str(monitoramento.dt_medicao ) 
        cd_usuario_inclusao_str = str(monitoramento.cd_usuario_inclusao )  
        dt_inclusao_str = str(monitoramento.dt_inclusao )  
        print(f'{cd_monitoramento_str.ljust(25) } | {cd_cultura_produto_sensor_str.ljust(25) } | {vlr_medido_str.ljust(25)} | {dt_medicao_str.ljust(25)} | {cd_usuario_inclusao_str.ljust(25)} | {dt_inclusao_str.ljust(25)}')

    @staticmethod
    def formartar_lista_retorno(monitoramentos):
        print(f'{'cd_monitoramento'.ljust(25)} | {'cd_cultura_produto_sensor'.ljust(25)} | {'vlr_medido'.ljust(25)} | {'dt_medicao'.ljust(25)} | {'cd_usuario_inclusao'.ljust(25)} | {'dt_inclusao'.ljust(25)}')
        for monitoramento in monitoramentos:                    
            cd_monitoramento_str = str(monitoramento.cd_monitoramento)         
            cd_cultura_produto_sensor_str = str(monitoramento.cd_cultura_produto_sensor )        
            vlr_medido_str = str(monitoramento.vlr_medido )  
            dt_medicao_str = str(monitoramento.dt_medicao ) 
            cd_usuario_inclusao_str = str(monitoramento.cd_usuario_inclusao )  
            dt_inclusao_str = str(monitoramento.dt_inclusao )  
            print(f'{cd_monitoramento_str.ljust(25) } | {cd_cultura_produto_sensor_str.ljust(25) } | {vlr_medido_str.ljust(25)} | {dt_medicao_str.ljust(25)} | {cd_usuario_inclusao_str.ljust(25)} | {dt_inclusao_str.ljust(25)}')  