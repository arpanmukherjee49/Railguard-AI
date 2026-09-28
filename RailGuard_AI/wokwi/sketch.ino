// RailGuard AI ESP32/Wokwi prototype.
// Pins: DHT22 DATA=4, MPU6050 SDA=21/SCL=22,
// current pot=34, load pot=35, LEDs=25/26/27.
// MQTT broker/topic match the Python demo.
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Wire.h>
#include <MPU6050.h>
#define DHT_PIN 4
#define DHT_TYPE DHT22
#define CURRENT_PIN 34
#define LOAD_PIN 35
#define NORMAL_LED 25
#define DEGRADING_LED 26
#define FAULT_LED 27
const char* WIFI_SSID="Wokwi-GUEST";
const char* WIFI_PASSWORD="";
const char* MQTT_BROKER="broker.hivemq.com";
const int MQTT_PORT=1883;
const char* MQTT_TOPIC="railguard/demo/traction_bearing";
DHT dht(DHT_PIN,DHT_TYPE); MPU6050 mpu; WiFiClient net; PubSubClient mqtt(net);
void setup(){Serial.begin(115200);pinMode(NORMAL_LED,OUTPUT);pinMode(DEGRADING_LED,OUTPUT);pinMode(FAULT_LED,OUTPUT);dht.begin();Wire.begin(21,22);mpu.initialize();WiFi.begin(WIFI_SSID,WIFI_PASSWORD);while(WiFi.status()!=WL_CONNECTED)delay(250);mqtt.setServer(MQTT_BROKER,MQTT_PORT);}
void loop(){if(!mqtt.connected()){String id="RailGuard-"+String(random(0xffff),HEX);while(!mqtt.connected())mqtt.connect(id.c_str());}mqtt.loop();float t=dht.readTemperature();int16_t ax,ay,az;mpu.getAcceleration(&ax,&ay,&az);float x=ax/16384.0,y=ay/16384.0,z=az/16384.0;float v=sqrt(x*x+y*y+z*z)*9.81;float current=analogRead(CURRENT_PIN)/4095.0*25.0;float load=analogRead(LOAD_PIN)/4095.0*100.0;if(isnan(t))t=0;String p="{\"temperature\":"+String(t,2)+",\"vibration\":"+String(v,2)+",\"current\":"+String(current,2)+",\"load\":"+String(load,2)+"}";mqtt.publish(MQTT_TOPIC,p.c_str());Serial.println(p);delay(2000);}
