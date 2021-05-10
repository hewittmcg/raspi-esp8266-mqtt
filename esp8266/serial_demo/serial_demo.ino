// Basic ESP8266 MQTT module.
// To be used as a demo to send data entered over serial.
// Based off the 2021-05-09 version of water_sensor_mqtt.
// NOTE: serial data must be sent with Newline enabled in the serial monitor.

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
const char* mqttServer = "192.168.0.204";
const int mqttPort = 2000;

const char* TX_TOPIC = "tx/";
const char* RX_TOPIC = "rx/";
const char* TX_JOIN_TOPIC = "tx/join/";
const char* RX_JOIN_TOPIC = "rx/join/";

const byte MSG_PREFIX = 0x01;
const byte JOIN_PREFIX = 0x02;

// Device ID, sent by server on join. -1 should never be sent as the device will recieve an ID from the network on join.
char* device_id = "0000";

// Locations of data blocks in RTC memory to persist beyond deepsleep.
// See https://www.espressif.com/sites/default/files/documentation/2c-esp8266_non_os_sdk_api_reference_en.pdf
// Note that each data block in the below valueshere represents a single 4-byte word.
// However, when accessing RTC memory, size must be given in bytes.
const uint32_t RTC_JOINED_LOCATION = 64;
const uint32_t RTC_ID_LOCATION = 66;

// Word set to signify that device has joined
const uint32_t RTC_JOINED_WORD = 0x4A6F686E;

// Moisture sensor pin (currently unused)
const int SENSOR_PIN = A0; 

WiFiClient nwk_client;
PubSubClient client(nwk_client);

void setup() {
  Serial.begin(9600);
  
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
  uint32_t temp_joined_word = 0;
  system_rtc_mem_read(RTC_JOINED_LOCATION, &temp_joined_word, 4);
  if(!memcmp(&temp_joined_word, &RTC_JOINED_WORD, 4)) {
    // Already joined, get ID from memory
    Serial.println("Device already joined network");
    system_rtc_mem_read(RTC_ID_LOCATION, device_id, 4);
    //Serial.println(device_id);
  }
  else {
    Serial.println("Device has not joined network, joining");
    // Request to be provisioned a device ID from the network
    client.subscribe(RX_JOIN_TOPIC);
    client.publish(TX_JOIN_TOPIC, &JOIN_PREFIX, 1);
    
    // Wait for message to be received, periodically check memory to 
    // see if callback function was called
    while(memcmp(&temp_joined_word, &RTC_JOINED_WORD, 4) != 0) {
      client.loop();
      system_rtc_mem_read(RTC_JOINED_LOCATION, &temp_joined_word, 4);
      delay(50);
    }
    Serial.println("Join complete");
  }
}

// Unused except to receive device ID from network on join
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.println("message arrived");
  // Check if join topic
  Serial.println(topic);
  
  if(strcmp(topic, RX_JOIN_TOPIC) == 0) {
    for(uint8_t i = 0; i < 4; i++) {
      device_id[i] = payload[i];
    }

    Serial.print("Received response to join request with device ID ");
    Serial.print(device_id);
    Serial.println(' ');
    // Write to RTC memory to store after deepsleep
    bool status = system_rtc_mem_write(RTC_JOINED_LOCATION, &RTC_JOINED_WORD, 4);
    if(!status) {
      Serial.println("WARNING - system_rtc_mem_write() failed writing RTC_JOINED_BYTE");
    }
    
    status = system_rtc_mem_write(RTC_ID_LOCATION, device_id, 4);
    if(!status) {
      Serial.println("WARNING - system_rtc_mem_write() failed writing device_id");
    }
  }
}

// Get serial input, send over MQTT
void loop() {
  Serial.println("Enter value to broadcast over MQTT");
  
  char buf[UINT8_MAX];
  uint8_t msg_len = 0;

  for(uint8_t i = 0; i < UINT8_MAX; i++) {
    while(!Serial.available());
    char rec = Serial.read();
    if(rec == '\n') { // EOM
      msg_len = i + 1; 
      buf[i] = '\0';
      break;
    }
    buf[i] = rec;
  }

  // Size of the below array should be equal to the sum of all n topics used to create it - n + 1 
  // to take account for null-terminating characters but avoid memory issues
  char topic_combined[9];
  
  // Form final topic
  strncpy(topic_combined, TX_TOPIC, 4);
  strncat(topic_combined, device_id, 4);

  // Need to allocate exact length to work with client.publish
  char *msg = new char[msg_len];
  memcpy(msg, buf, msg_len);
  
  // Send data
  Serial.println("Sending message...");
  Serial.print("Topic:");
  Serial.println(topic_combined);
  Serial.print("Message:");
  Serial.println(msg);
  
  client.publish(topic_combined, msg);
  
  delete msg;
} 
