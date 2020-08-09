// Basic ESP8266 MQTT module.
// To be used to periodically send data from a moisture sensor

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// For RTC memory access functions
extern "C" {
  #include "user_interface.h"
}

// WiFi info
const char *ssid = "";
const char *pass = "";

// MQTT info, topics, message prefixes
const char* mqttServer = "192.168.2.26";
const int mqttPort = 2000;

const char* TX_TOPIC = "tx/";
const char* RX_TOPIC = "rx/";
const char* TX_JOIN_TOPIC = "tx/join/";
const char* RX_JOIN_TOPIC = "rx/join/";

const byte MSG_PREFIX = 0x01;
const byte JOIN_PREFIX = 0x02;

// Device ID, sent by server on join. -1 should never be sent as the device will recieve an ID from the network on join.
char* device_id = "-1";

// Locations of data blocks in RTC memory to persist beyond deepsleep.
// See https://www.espressif.com/sites/default/files/documentation/2c-esp8266_non_os_sdk_api_reference_en.pdf
const uint32_t RTC_JOINED_LOCATION = 64;
const uint32_t RTC_ID_LOCATION = 66;
// Word set to signify that device has joined
const byte RTC_JOINED_BYTE[4] = {0x4A, 0x6F, 0x68, 0x6E};

// Moisture sensor pin (currently unused)
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

  // Check if device has already joined
  byte temp_joined_byte[4];
  system_rtc_mem_read(RTC_JOINED_LOCATION, &temp_joined_byte, 4);
  if(!memcmp(temp_joined_byte, RTC_JOINED_BYTE, 4)) {
    // Already joined, get ID from memory
    Serial.println("Device already joined network");
    system_rtc_mem_read(RTC_ID_LOCATION, device_id, 2);
    //Serial.println(device_id);
  }
  else {
    Serial.println("Device has not joined network, joining");
    // Request to be provisioned a device ID from the network
    client.subscribe(RX_JOIN_TOPIC);
    client.publish(TX_JOIN_TOPIC, &JOIN_PREFIX, 1);
    
    // Wait for message to be received, periodically check memory to 
    // see if callback function was called
    while(memcmp(temp_joined_byte, RTC_JOINED_BYTE, 4) != 0) {
      client.loop();
      system_rtc_mem_read(RTC_JOINED_LOCATION, &temp_joined_byte, 4);
      delay(50);
    }
  }
}

// Unused except to receive device ID from network on join
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.println("message arrived");
  // Check if join topic
  Serial.println(topic);
  
  if(strcmp(topic, RX_JOIN_TOPIC) == 0) {
    Serial.print("Received response to join request with device ID ");
    Serial.print((char*)payload);
    Serial.println(' ');
    device_id = (char*)payload;
    // Write to RTC memory to store after deepsleep
    system_rtc_mem_write(RTC_ID_LOCATION, device_id, 2);
    system_rtc_mem_write(RTC_JOINED_LOCATION, RTC_JOINED_BYTE, 4);
  }
}

// Get water sensor measurement, send over MQTT
void loop() {
  // Test values.  Note: will be sent little endian
  byte tx_payload[2] = {MSG_PREFIX, 0xFF};

  int temp = 0;
  char payload_char[5];
  // Size of the below array should be equal to the sum of all n topics used to create it - n + 1 
  // to take account for null-terminating characters but avoid memory issues
  char topic_combined[9];
  // Copy bytes to int
  memcpy(&temp, tx_payload, sizeof(tx_payload));
  // Convert int to hex string
  itoa(temp, payload_char, 16);
  // Form final topic
  strncpy(topic_combined, TX_TOPIC, 4);
  strncat(topic_combined, device_id, 4);

  // Send data
  client.publish(topic_combined, payload_char);
  delay(1000); 
} 
