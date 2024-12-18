#include <Servo.h>

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define OLED_RESET 4

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
Adafruit_SSD1306 display(OLED_RESET);
int p2 = 0;
int p2_lo;
int p2_hi;
int curTime;

int pos;
int LEFT_SERVO_UP = 1;
int RIGHT_SERVO_UP = 189;
int LEFT_SERVO_DOWN = 90;
int RIGHT_SERVO_DOWN = 90;
int refAngle = 96;

int leftServoPin = 6;
int rightServoPin = 5;
int touchSensorPin = 3;
int ledPin = 13;

bool flag = false;

bool activation = false;
bool actvSuccess = false;
int actvState = 1;
int counter = 0;
String jarvisActivationStr = "~JARVIS ACTIVATED~";

String receivedText;
// Connect Touch sensor on Digital Pin 2
Servo leftServo;
Servo rightServo;

void setup() {
  Serial.begin(9600);
  pinMode(touchSensorPin, INPUT);       //Set touch sensor pin to input mode
  pinMode(ledPin, OUTPUT);
  leftServo.attach(leftServoPin);
  rightServo.attach(rightServoPin);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // initialize with the I2C addr 0x3C (for the 128x32)

  p2_lo = random(3,7);
  p2_hi = random(90,97);
}
 
void loop() {
  display.clearDisplay();

  if (Serial.available() > 0) {
    receivedText = Serial.readStringUntil("\n");
    Serial.println(receivedText);
    if (receivedText == "<Activate Jarvis>\n") {
      activation = true;
      Serial.println("Jarvis: Activating..."); 
    }

    else if (receivedText == "<Deactivate Jarvis>\n") {
      activation = false;
      actvSuccess = false;
      Serial.println("Jarvis: Deactivating..."); 
    }
    
    else if (receivedText == "Open helmet\n") {
      flag = true;
      Serial.println("Jarvis: Opening helmet"); 
    }
    else if (receivedText == "Close helmet\n") {
      Serial.println("Jarvis: Closing helmet"); 
      flag = false;
    }
  }

  if(digitalRead(touchSensorPin)==HIGH) {      // Read Touch sensor signal
    flag = !flag;
    Serial.println("Actuating helmet");
    delay(30);  
  }

  if (activation == true) {
    digitalWrite(ledPin, HIGH);
    if (actvSuccess == false) {
      // Play the activation animation on the OLED display. Move this into a custom library OLED_Progress_Bar.h
      //==================================================
      if (actvState == 1) {
        drawPercentbar(0, 10, 100, 15, p2);
        display.display();
        p2++;
    
        if(p2 > 100) {
          p2 = 0;
          actvState = 2;
        }
        
        else if (p2 == p2_lo) { // lo jump point
          delay(random(50,300));
          p2 = p2_hi; // hi jump point
          delay(random(50,150));
        }
        delay(3);
      }
  
      else if (actvState == 2) {
        if (counter > jarvisActivationStr.length()) {
          actvState = 3;
        }
        else {  
          display.clearDisplay();    
          display.setTextSize(1);
          display.setTextColor(WHITE);
          display.setCursor(0, 10);
          display.println(jarvisActivationStr.substring(0,counter));
          Serial.println(counter);
          counter++;
          delay(40);
        }
      }
  
      else if (actvState == 3) {
        testdrawtriangle();
        actvSuccess = true; // ACTIVATION SUCCESSFUL

      }
      
//      display.display();
      //==================================================
      
    }
    
    if(flag == true) { 
      leftServo.write(LEFT_SERVO_UP);
      rightServo.write(RIGHT_SERVO_UP);
//      for (pos = 0; pos <= 89; pos += 1) { // goes from 180 degrees to 0 degrees
//        rightServo.write(refAngle + pos);              // tell servo to go to position in variable 'pos'
//        leftServo.write(refAngle - pos);
//        delay(12);                       // waits 15 ms for the servo to reach the position
//      }
      delay(200);
  
   }
    else {
//      for (pos = 89; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
//        rightServo.write(refAngle + pos);              // tell servo to go to position in variable 'pos'
//        leftServo.write(refAngle - pos);
//        delay(12);                       // waits 15 ms for the servo to reach the position
//      }
      leftServo.write(LEFT_SERVO_DOWN);
      rightServo.write(RIGHT_SERVO_DOWN);
      delay(200);
   }
  }

  else {
    curTime = millis() % 2000; 
    digitalWrite(ledPin, LOW);
    // "Idling" animation on the OLED Display
    if (curTime < 500) display.fillCircle(32, 16, 2, WHITE);
    if (curTime < 1000) display.fillCircle(64, 16, 2, WHITE);
    if (curTime < 1500) display.fillCircle(96, 16, 2, WHITE);
   
//    for (int i = 0; i < 3; i++) {
//      display.fillCircle(42 + (i*42), 16, 2, WHITE);
//      delay(500);
//    }
  }
  display.display();

}


void testdrawtriangle(void) {
  display.clearDisplay();

  for(int16_t i=0; i<max(display.width(),display.height())/2; i+=5) {
    display.drawTriangle(
      display.width()/2  , display.height()/2-i,
      display.width()/2-2*i, display.height()/2+i,
      display.width()/2+2*i, display.height()/2+i, WHITE);
    display.display();
    delay(1);
  }

  delay(200);
}

void drawPercentbar(int x,int y, int width,int height, int progress) {
  progress = progress > 100 ? 100 : progress;
  progress = progress < 0 ? 0 : progress;
  float bar = ((float)(width-4) / 100) * progress; 
  
  display.drawRect(x, y, width, height, WHITE);
  display.fillRect(x+2, y+2, bar , height-4, WHITE);
  
  // Display progress text
  if( height >= 15){
    display.setCursor((width/2) -3, y+5 );
    display.setTextSize(1);
    display.setTextColor(WHITE);

   if( progress >= 50)
     display.setTextColor(BLACK, WHITE); // 'inverted' text
     display.print(progress);
     display.print("%");
  }

}
