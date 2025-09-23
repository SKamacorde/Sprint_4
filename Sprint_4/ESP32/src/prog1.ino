#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include <WiFiUdp.h>

#define DHT_PIN 23
#define DHT_TYPE DHT22
#define IDENTIFICADOR 1
#define NUMERO_SERIE 1234567


DHT dht(DHT_PIN, DHT_TYPE);
WiFiClient espClient;
PubSubClient client(espClient);

// Configurações NTP
WiFiUDP udp;
unsigned int localPort = 2390;  // Porta local
byte NTPServer[] = { 129, 6, 15, 28 }; // Servidor NTP
const int NTP_PACKET_SIZE = 48; // Tamanho do pacote NTP
byte packetBuffer[NTP_PACKET_SIZE]; // Buffer do pacote NTP

const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_client_id = "ESP32GuardiaoNatural_Python_99";
const char* mqtt_topic = "guardiao_natural/sensor_data";

const char* ssid = "Wokwi-GUEST";
const char* password = "";

float temperatura = 0.0;
float umidade = 0.0;

void setup_wifi() {
  delay(10);
  Serial.print("Conectando a "); Serial.println(ssid);
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi conectado!");
    Serial.print("Endereco IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n❌ Falha ao conectar WiFi.");
  }
}

void sendNTPRequest() {
  // Preenche o pacote com as informações NTP
  memset(packetBuffer, 0, NTP_PACKET_SIZE);
  packetBuffer[0] = 0b11100011; // Inicialização do pacote
  udp.begin(localPort);
  udp.beginPacket(NTPServer, 123);  // Porta 123 é usada para NTP
  udp.write(packetBuffer, NTP_PACKET_SIZE);
  udp.endPacket();
}

unsigned long getNTPTime() {
  sendNTPRequest();
  delay(1000); // Espera o servidor NTP responder

  if (udp.parsePacket()) {
    udp.read(packetBuffer, NTP_PACKET_SIZE);
    unsigned long highWord = word(packetBuffer[43], packetBuffer[42]);
    unsigned long lowWord = word(packetBuffer[47], packetBuffer[46]);
    unsigned long time = highWord << 16 | lowWord; // Junta os dois valores
    return time - 2208988800UL; // Ajuste para o Unix epoch
  }
  return 0;
}


String getDateTimeString() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("❌ Falha ao obter hora via NTP");
    return "";
  }

  // Simula os milissegundos (não é precisão real de relógio)
  unsigned long ms = millis() % 1000;

char buffer[40];
 snprintf(buffer, sizeof(buffer), 
    "%04d-%02d-%02d %02d:%02d:%02d",
    timeinfo.tm_year + 1900,
    timeinfo.tm_mon + 1,
    timeinfo.tm_mday,
    timeinfo.tm_hour,
    timeinfo.tm_min,
    timeinfo.tm_sec
);
  return String(buffer);
}

void reconnect_mqtt() {
  while (!client.connected()) {
    Serial.print("Tentando conexao MQTT...");
    if (client.connect(mqtt_client_id)) {
      Serial.println("Conectado!");
    } else {
      Serial.print("Falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);
  dht.begin();
  setup_wifi();
  configTime(0, 0, "pool.ntp.org");
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect_mqtt();
  }
  client.loop();

  umidade = dht.readHumidity();
  temperatura = dht.readTemperature();

  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("❌ Falha ao ler do sensor DHT!");
    return;
  }

  unsigned long timestamp = getNTPTime();
 String datetime = getDateTimeString();

  StaticJsonDocument<384> doc;
  doc["UMIDADE"] = umidade;
  doc["TEMPERATURA"] = temperatura;
  doc["NUMERO_SERIE"] = NUMERO_SERIE; 
  doc["IDENTIFICADOR"] = IDENTIFICADOR;
  doc["DATA_MEDICAO"] = datetime;
 

  String payload;
  serializeJson(doc, payload);

  Serial.println("⏺️ Publicando dados MQTT...");
  Serial.print("Tópico: "); Serial.println(mqtt_topic);
  Serial.print("Payload: "); Serial.println(payload);

  bool published = client.publish(mqtt_topic, payload.c_str());
  if (published) {
    Serial.println("✅ Publicação MQTT bem-sucedida.");
  } else {
    Serial.print("❌ Falha na publicação MQTT. Estado: ");
    Serial.println(client.state());
  }

  delay(5000); // Aguarda 5 segundos antes de publicar novamente
}
