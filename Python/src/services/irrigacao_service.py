from tabulate import tabulate
class IrrigacaoService:


    def __init__(self, meteorologia_service) :
          self.meteorologia_service = meteorologia_service

    def irrigar_plantacao(self): 
        limite_chuva = 20  # limite percentual para ligar/desligar bomba       

        # Buscando dados da meteorolia
        df = self.meteorologia_service.obter_dados_meteorologia()

        # Máxima probabilidade por dia
        max_por_dia = df.groupby("Data")["Probabilidade (%)"].max().reset_index()
        max_por_dia["Bomba de Irrigação"] = max_por_dia["Probabilidade (%)"].apply(
        lambda x: "Desligada" if x > limite_chuva else "Ligada"
        )

        print(tabulate(max_por_dia, headers="keys", tablefmt="grid"))
        
