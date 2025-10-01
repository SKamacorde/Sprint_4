# main.py
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from src.service_factory import get_monitoramento_service, get_cultura_produto_sensor_configuracao_service
from src.integrations.mqqt import mqtt_client

# # ==================================
# # 1. Inicialização do Cliente MQTT ---
# # ==================================

def on_message(client, userdata, msg):
    print("📥 Mensagem recebida!")
    print(f"Tópico: {msg.topic}")
    print(f"Payload bruto: {msg.payload}")

    try:
        data = json.loads(msg.payload.decode())
        print(f"📦 Payload processado: {data}")
        monitoramento_service = get_monitoramento_service()
        monitoramento_service.inserir_monitoramento(data['IDENTIFICADOR'] ,data['UMIDADE'], data['DATA_MEDICAO'] ,  data['NUMERO_SERIE'] )        
    except json.JSONDecodeError:
        print("❌ Erro ao decodificar JSON da mensagem MQTT.")
    except Exception as e:
        print(f"❌ Erro no processamento da mensagem: {e}")

if __name__ == "__main__":
    mqtt_client = mqtt_client.MqttClient(on_message_callback=on_message)
    mqtt_client.start()


# monitoramento_service = get_monitoramento_service()
# configuracao_service = get_cultura_produto_sensor_configuracao_service()

# ###  Buscar os registro  do sensor de umidade para a cultura cafe
# cd_monitoramento = 1  
# ### Sensores registram leituras a cada hora, armazenadas em `TBL_MONITORAMENTO`.
# monitoramentos = monitoramento_service.listar_monitoramentos(cd_monitoramento)
# valores = [m.vlr_medido for m in monitoramentos]
# df = pd.DataFrame({ "vlr_medido": valores})

# ### O sistema compara leituras com valores mínimo/máximo definidos em `TBL_CULTURA_PRODUTO_SENSOR_CONFIGURACAO` para sugerir ajustes.
# # Criar classes: Baixa, Média, Alta
# configuracao = configuracao_service.obter_configuracao(cd_monitoramento)
# df["classe"] = pd.cut(
#     df["vlr_medido"],
#     bins=[-1, configuracao.vlr_minimo, configuracao.vlr_maximo, 100],
#     labels=["Abaixo do mínimo", "Entre min e max", "Acima do máximo"]
# )

# # Agrupamento das classes: Baixa, Média, Alta
# print("Distribuição das classes:")
# print(df['classe'].value_counts())

# # ==================================
# # 2. CLASSIFICAÇÃO
# # ==================================
# X_cls = df[["vlr_medido"]]
# y_cls = df["classe"]

# #  RandomForestClassifier → cria um classificador baseado em Random Forest, que é um conjunto de árvores de decisão.
# #  n_estimators=100 → o modelo vai criar 100 árvores; mais árvores geralmente melhoram a estabilidade, mas aumentam o tempo de treinamento.
# #  random_state=42 → garante reprodutibilidade; sempre que rodar com a mesma seed, os resultados serão iguais
# model_cls = RandomForestClassifier(n_estimators=100, random_state=42)

# # Verifica tamanho do dataset
# Xc_train, Xc_test, yc_train, yc_test = train_test_split(
#     X_cls, y_cls, test_size=0.2, random_state=42, stratify=y_cls
# )
# model_cls.fit(Xc_train, yc_train)
# yc_pred = model_cls.predict(Xc_test)

# # Avaliação
# print(f"Acurácia do modelo de classificação: {accuracy_score(yc_test, yc_pred):.2f}")

# # ==================================
# # 3. EXIBIR GRÁFICOS EM UMA ÚNICA JANELA
# # ==================================
# fig, axes = plt.subplots(1, 2, figsize=(18, 6))
# # 3.1 Matriz de Confusão
# cm = confusion_matrix(yc_test, yc_pred, labels=["Abaixo do mínimo", "Entre min e max", "Acima do máximo"])
# ConfusionMatrixDisplay(cm, display_labels=["Abaixo do mínimo", "Entre min e max", "Acima do máximo"]).plot(
#     cmap="Blues", ax=axes[0], colorbar=False
# )
# axes[0].set_title("Matriz de Confusão - Classificação de Umidade")

# # 3.2 Real vs Predito
# axes[1].scatter(Xc_test, yc_test, color="blue", label="Real")
# axes[1].scatter(Xc_test, yc_pred, color="red", alpha=0.6, label="Predito")
# axes[1].set_xlabel("Valor Medido")
# axes[1].set_ylabel("Classe")
# axes[1].set_title("Classificação de Níveis de Umidade")
# axes[1].legend()
# plt.show()
