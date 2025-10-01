from dash import Dash, dcc, html
import plotly.express as px
from dash.dependencies import Output, Input
import pandas as pd
from src.service_factory import get_monitoramento_service

if __name__ == "__main__":    
    # Obtém os dados
    monitoramento_service = get_monitoramento_service()
    monitoramentos = monitoramento_service.listar_monitoramentos()

    if not monitoramentos:
        print("Nenhum monitoramento encontrado.")
    else:
        # Cria DataFrame com os dados
        df = pd.DataFrame([{
            "CD_CULTURA_PRODUTO_SENSOR": m.cd_cultura_produto_sensor,
            "VLR_MEDIDO": m.vlr_medido,
            "DT_MEDICAO": m.dt_medicao,
            "CD_USUARIO_INCLUSAO": m.cd_usuario_inclusao
        } for m in monitoramentos])

        # Converte DT_MEDICAO para datetime e ordena
        df["DT_MEDICAO"] = pd.to_datetime(df["DT_MEDICAO"], dayfirst=True)

        # Mapeia nomes dos sensores
        sensor_nome = {
            1: "Café Umidade"           
        }

        # Aplica mapeamento
        df['SENSOR'] = df['CD_CULTURA_PRODUTO_SENSOR'].map(sensor_nome)
        valid_sensors = df['SENSOR'].dropna().unique()      
        # Inicializa o app Dash
        app = Dash(__name__)
        app.title = "Dashboard sensor de umidade"

        # Layout do dashboard
        app.layout = html.Div([
            html.H1("📊 Dashboard sensor de umidade "),
            dcc.Dropdown(
                id='sensor-selector',
                options=[{'label': nome, 'value': nome} for nome in valid_sensors],
                value="Café Umidade",  # Valor padrão
                clearable=False,
                style={'width': '50%'}
            ),
            dcc.Graph(id='sensor-graph'),
            html.Div(id="descricao", style={'marginTop': '20px', 'fontSize': '16px'})
        ])

        # Callback do gráfico
        @app.callback(
            [Output('sensor-graph', 'figure'),
             Output('descricao', 'children')],
            [Input('sensor-selector', 'value')]
        )
        def atualizar_grafico(sensor):
            dff = df[df['SENSOR'] == sensor].copy()

            if dff.empty:
                fig = px.bar(title="Nenhum dado encontrado para esse sensor.")
                return fig, "Nenhum dado disponível para este sensor."

            # Garantir ordenação por data
            dff["DT_MEDICAO"] = pd.to_datetime(dff["DT_MEDICAO"], errors="coerce")
            dff = dff.sort_values("DT_MEDICAO")

            # Gráfico de barras verticais (default)
            fig = px.bar(
                dff,
                x="DT_MEDICAO",
                y="VLR_MEDIDO",
                title=f"{sensor} ao longo do tempo"
            )

            fig.update_layout(
                xaxis_title="Data da Medição",
                yaxis_title=sensor,
                template="plotly_white"
            )

            descricao = f"O gráfico acima mostra os valores de {sensor.lower()} registrados ao longo do tempo."
            if sensor == "Status da Bomba":
                descricao += " Valor 1 indica bomba LIGADA e 0 indica DESLIGADA."

            return fig, descricao

        
        # Executa o servidor local
        app.run(debug=True)
