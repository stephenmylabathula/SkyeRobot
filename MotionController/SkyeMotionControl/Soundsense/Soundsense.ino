int left = 0;  // variable to store the value coming from the sensor
int right = 0;

void setup() {
}

void loop() {
  right = analogRead(A0);
  left = analogRead(A1);
  if (left < 100 || right < 100){
    if (left > right)
      Serial.println("Left: " + String(float(left)/float(right)));
    else if (right > left)
      Serial.println("Right: " + String(float(right)/float(left)));
    else
      Serial.println("Center");
    delay(1000);
  }
    
}
