# main.py
import json
from src.service_factory import get_monitoramento_service
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