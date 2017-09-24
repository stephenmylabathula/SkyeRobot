#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN            3
#define NUMPIXELS      12
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixel = Adafruit_NeoPixel(NUMPIXELS, 13, NEO_GRB + NEO_KHZ800);

int delayval = 30; // delay for half a second

void setup() {
  pixels.begin();
}

void blinkDown(){
    pixels.setPixelColor(9, pixels.Color(0,0,0));
    pixels.setPixelColor(10, pixels.Color(0,0,0));
    pixels.setPixelColor(3, pixels.Color(0,0,0));
    pixels.setPixelColor(4, pixels.Color(0,0,0));
    pixel.setPixelColor(9, pixels.Color(0,0,0));
    pixel.setPixelColor(10, pixels.Color(0,0,0));
    pixel.setPixelColor(3, pixels.Color(0,0,0));
    pixel.setPixelColor(4, pixels.Color(0,0,0));
    pixels.show();
    pixel.show();
    delay(delayval);

    pixels.setPixelColor(8, pixels.Color(0,0,0));
    pixels.setPixelColor(11, pixels.Color(0,0,0));
    pixels.setPixelColor(2, pixels.Color(0,0,0));
    pixels.setPixelColor(5, pixels.Color(0,0,0));
    pixel.setPixelColor(8, pixels.Color(0,0,0));
    pixel.setPixelColor(11, pixels.Color(0,0,0));
    pixel.setPixelColor(2, pixels.Color(0,0,0));
    pixel.setPixelColor(5, pixels.Color(0,0,0));
    pixels.show();
    pixel.show();
    delay(delayval);

    pixels.setPixelColor(7, pixels.Color(0,0,0));
    pixels.setPixelColor(0, pixels.Color(0,0,0));
    pixels.setPixelColor(1, pixels.Color(0,0,0));
    pixels.setPixelColor(6, pixels.Color(0,0,0));
    pixel.setPixelColor(7, pixels.Color(0,0,0));
    pixel.setPixelColor(0, pixels.Color(0,0,0));
    pixel.setPixelColor(1, pixels.Color(0,0,0));
    pixel.setPixelColor(6, pixels.Color(0,0,0));
    pixels.show();
    pixel.show();
    delay(delayval);
}


void blinkUp(){

    pixels.setPixelColor(7, pixels.Color(0,0,255));
    pixels.setPixelColor(0, pixels.Color(0,0,255));
    pixels.setPixelColor(1, pixels.Color(0,0,255));
    pixels.setPixelColor(6, pixels.Color(0,0,255));
    pixel.setPixelColor(7, pixels.Color(0,0,255));
    pixel.setPixelColor(0, pixels.Color(0,0,255));
    pixel.setPixelColor(1, pixels.Color(0,0,255));
    pixel.setPixelColor(6, pixels.Color(0,0,255));
    pixels.show();
    pixel.show();
    delay(delayval);

    pixels.setPixelColor(8, pixels.Color(0,0,255));
    pixels.setPixelColor(11, pixels.Color(0,0,255));
    pixels.setPixelColor(2, pixels.Color(0,0,255));
    pixels.setPixelColor(5, pixels.Color(0,0,255));
    pixel.setPixelColor(8, pixels.Color(0,0,255));
    pixel.setPixelColor(11, pixels.Color(0,0,255));
    pixel.setPixelColor(2, pixels.Color(0,0,255));
    pixel.setPixelColor(5, pixels.Color(0,0,255));
    pixel.show();
    pixels.show();
    delay(delayval);
    
    pixels.setPixelColor(9, pixels.Color(0,0,255));
    pixels.setPixelColor(10, pixels.Color(0,0,255));
    pixels.setPixelColor(3, pixels.Color(0,0,255));
    pixels.setPixelColor(4, pixels.Color(0,0,255));
    pixel.setPixelColor(9, pixels.Color(0,0,255));
    pixel.setPixelColor(10, pixels.Color(0,0,255));
    pixel.setPixelColor(3, pixels.Color(0,0,255));
    pixel.setPixelColor(4, pixels.Color(0,0,255));
    pixels.show();
    pixel.show();
    delay(delayval);
}

void loop() {
    delay(3000);
    blinkDown();
    delay(50);
    blinkUp();
    //delay(10);
    //blinkDown();
    //delay(100);
    //blinkUp();
}
