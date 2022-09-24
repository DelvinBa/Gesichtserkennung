#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>
#include <Adafruit_NeoPixel.h>

const char* PASSWORD = "Hack2022!";
const char* SSID = "Forum";
const char* MQTT_BROKER = "172.16.2.5";

int servostate = 0;
int rot = 0;
int gruen = 0;
const int NUMPIXELS = 8;
int PIN = 5;

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

WiFiClient espClient;
PubSubClient client(espClient);

Servo servoblau;

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      //client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("securedoor/face");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  servostate = servoblau.read();
  pixels.clear();
  if ((char)payload[0] == '1') {
    rot = 0;
    gruen = 255;
    servoblau.write(servostate+180);
    Serial.println("erkannt");
  }
  else if ((char)payload[0] == '0') {
    rot = 255;
    gruen = 255;
  }
  else if ((char)payload[0] == '2') {
    rot = 255;
    gruen = 0;
  }
  else if ((char)payload[0] == '3') {
    rot = 0;
    gruen = 0;
  }
  for (int i = 0; i < NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(rot, gruen, 0));
  }
  pixels.show();
}

void setup() {
  Serial.begin(115200);
  Serial.println("Programm gestartet");
  
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  client.setServer(MQTT_BROKER, 1883);
  client.setCallback(callback);

  servoblau.attach(12);

  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  pixels.setBrightness(25);
}
void loop() {
    if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
