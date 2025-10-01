import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
load_dotenv()

class MqttClient:
    # Configuração do Cliente MQTT
    def __init__(self, on_message_callback):   

        # Busca no arquivo .env as configurações do servidor mqtt
        # MQTT_BROKER_HOST SERVIDOR 
        # MQTT_TOPIC_ALL_DATA TOPICO 
        # MQTT_BROKER_PORT PORTA 
        self.broker = os.getenv('MQTT_BROKER_HOST')       
        self.topic = os.getenv('MQTT_TOPIC_ALL_DATA')   
        self.port = int(os.getenv('MQTT_BROKER_PORT', 1883))

        if not self.broker or not self.topic:
            raise ValueError("❌ Variáveis de ambiente não definidas corretamente.")

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = on_message_callback  # <<< Aqui está o callback vindo de fora

        self.client.reconnect_delay_set(min_delay=1, max_delay=60)

        print(f"🔌 Conectando ao broker MQTT: {self.broker}:{self.port}")
        try:
            self.client.connect(self.broker, self.port, 60)
        except Exception as e:
            print(f"❌ Não foi possível conectar ao broker MQTT: {e}")
            exit()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"✅ Conectado com sucesso ao broker MQTT.")
            client.subscribe(self.topic)
            print(f"📡 Inscrito no tópico: {self.topic}")
        else:
            print(f"❌ Falha na conexão. Código de retorno: {rc}")

    def start(self):
        print("🚀 Iniciando loop MQTT...")
        self.client.loop_forever()
