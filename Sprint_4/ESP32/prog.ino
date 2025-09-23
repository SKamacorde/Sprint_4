#include <WiFi.h>

// Configurações da Rede Wi-Fi
const char* ssid = "seu SSID";  // Substitua pelo SSID da rede Wi-Fi
const char* password = "SUA SENHA";         // Substitua pela senha da rede (senha vazia no Wokwi-GUEST)

void setup() {
  Serial.begin(115200);  // Inicializa o Monitor Serial
  delay(1000);

  Serial.println("Conectando ao Wi-Fi...");

  // Inicia a conexão ao Wi-Fi
  WiFi.begin(ssid, password);

  // Aguarda a conexão
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Exibe informações da conexão
  Serial.println("\nWi-Fi conectado!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Obtém a intensidade do sinal (RSSI) em dBm
  int rssi = WiFi.RSSI();  // Lê a força do sinal da rede atual

  // Exibe a intensidade no Monitor Serial
  Serial.print("Intensidade do sinal Wi-Fi (RSSI): ");
  Serial.print(rssi);
  Serial.println(" dBm");

  delay(2000);  // Atualiza a leitura a cada 2 segundos
}