#define timeSeconds 10
#define BUZZER 14
#define motionSensor 33
#include "WiFi.h"
#include "ESPAsyncWebSrv.h"
#include <ESP32Servo.h>

#define SERVO_PIN 27

Servo servoMotor;
int mins = 500;
int maxs = 2400;
ESP32PWM pwm;

bool active = false;
 
AsyncWebServer server(80);

void serverListen(){

/*
  // Set your Static IP address
  IPAddress local_IP(192, 168, 255, 69);
  // Set your Gateway IP address
  IPAddress gateway(192, 168, 255, 204); //input gateway and subnet
  IPAddress subnet(255, 255, 255, 0);
  IPAddress primaryDNS(192, 168, 225, 204);
  IPAddress secondaryDNS(0, 0, 0, 0);

  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    Serial.println("STA Failed to configure");
  } */

  
  
  WiFi.begin("Martin Router Ping", "Pineapple");
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

 
  Serial.println(WiFi.localIP());
  Serial.println(WiFi.gatewayIP());
  Serial.println(WiFi.subnetMask());
 
  server.on(
    "/post",
    HTTP_POST,
    [](AsyncWebServerRequest * request){},
    NULL,
    [](AsyncWebServerRequest * request, uint8_t *data, size_t len, size_t index, size_t total) {
      
      for (size_t i = 0; i < len; i++) {
        Serial.write(data[i]);
        if (i == 9){
          if (data[i] == '8'){
            active = true;
          } else {
            active = false;
          }
        }
      }
 
 
      request->send(200);
  });
 
  server.begin();
}


// Timer: Auxiliary variables
unsigned long now = millis();
unsigned long now1 = millis();
unsigned long now2 = millis();
unsigned long lastTrigger = 0;
bool led_stat = false;
bool annoying = false;
boolean startTimer = false;



// Checks if motion was detected, sets LED HIGH and starts a timer
void IRAM_ATTR detectsMovement() {
  if (active){
    Serial.println("MOTION DETECTED!!!");
    ledcWriteTone(3,370);
    startTimer = true;
    lastTrigger = millis();
    Serial.print(now2);
    Serial.print(',');
    Serial.println(lastTrigger);
    annoying = true;

    

    servoMotor.write(30);
  }
}

void setup() {
  
  pinMode(32, OUTPUT);
    
  // Serial port for debugging purposes
  Serial.begin(115200);

  serverListen();
  
  ledcSetup(3, 8000, 14);
  // Attach BUZZER pin.
  ledcAttachPin(BUZZER, 3);
  
  // PIR Motion Sensor mode INPUT_PULLUP
  pinMode(motionSensor, INPUT_PULLUP);
  // Set motionSensor pin as interrupt, assign interrupt function and set RISING mode
  attachInterrupt(digitalPinToInterrupt(motionSensor), detectsMovement, RISING);

  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  servoMotor.setPeriodHertz(50);
  
  servoMotor.attach(SERVO_PIN, mins, maxs);
  delay(1500);
  servoMotor.write(150);
}

void loop() {
  delay(250);
  now2 = millis();
  if (annoying) {
      if (now2 - now > 150 && led_stat == 0){
        digitalWrite(32, HIGH);
        led_stat = 1;
      }
  
      if (now2 - now > 650){
        digitalWrite(32, LOW);
        led_stat = 0;
        now = now2;
      }
  }

    // Current time
    
  
    if(startTimer && (now2 - lastTrigger > (timeSeconds*1000))) {
      ledcWriteTone(3,0);
      startTimer = false;
      servoMotor.write(150);
      annoying = false;
      digitalWrite(32, LOW);
    
      


    }
}
