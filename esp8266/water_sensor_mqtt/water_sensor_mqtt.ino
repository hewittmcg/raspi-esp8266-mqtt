// Basic ESP8266 MQTT module.
// To be used to periodically send data from a moisture sensor

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi info
const char *ssid = "VIRGIN892";
const char *pass = "!Algonquin99";

// MQTT info, topics, message prefixes
const char* mqttServer = "192.168.2.26";
const int mqttPort = 2000;
const char* TX_TOPIC = "tx/";
const char* RX_TOPIC = "rx/";
const char* JOIN_TOPIC = "join/";
const byte MSG_PREFIX = 0x01;
const byte JOIN_PREFIX = 0x02;

// Device ID, sent by server on join. Temp value for testing, formatted as char for convenience
char device_id[5] = "1337";

// Locations of data blocks in RTC memory to persist beyond deepsleep.
// See https://www.espressif.com/sites/default/files/documentation/2c-esp8266_non_os_sdk_api_reference_en.pdf
const uint32_t RTC_JOINED_LOCATION = 64;
const uint32_t RTC_ID_LOCATION = 66;
// Word set to signify that device has joined
const byte RTC_JOINED_BYTE[4] = {0x4A, 0x6F, 0x68, 0x6E};

// Moisture sensor pin
const int SENSOR_PIN = A0; 

WiFiClient nwk_client;
PubSubClient client(nwk_client);

void setup() {
  Serial.begin(115200);
  
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, pass);
  while(WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print('.');
  }
  Serial.println(' ');
  Serial.println("Connected to WiFi");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  
  Serial.print("Connecting to MQTT");
  while(!client.connected()) {
    delay(250);
    Serial.print('.');
    client.connect("testid");
  }
  
  Serial.println(' ');
  Serial.println("Connected to MQTT Broker");
}

// Unused currently, will be used to implement receiving device ID
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("message arrived");
}

// Get water sensor measurement, send over MQTT
void loop() {
  client.loop();
  // Test values.  Note: will be sent little endian
  byte tx_payload[2] = {MSG_PREFIX, 0xFF};

  int temp = 0;
  char payload_char[5];
  char topic_combined[15];
  // Copy bytes to int
  memcpy(&temp, tx_payload, sizeof(tx_payload));
  // Convert int to hex string
  itoa(temp, payload_char, 16);

  // Append device ID to topic
  strcpy(topic_combined, TX_TOPIC);
  strcat(topic_combined, device_id);
  // Send data
  client.publish(topic_combined, payload_char);
  delay(1000); 
} 
