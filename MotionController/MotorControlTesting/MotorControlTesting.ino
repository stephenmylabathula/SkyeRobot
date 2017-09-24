//Standard PWM DC control
int E1 = 5;     //M1 Speed Control
int M1 = 4;    //M1 Direction Control

void back_off (char a,char b)          //Move backward
{
  analogWrite (E1,a);
  digitalWrite(M1,LOW);  
}

void stop(void)                    //Stop
{
  digitalWrite(E1,LOW);     
} 

void setup(void) 
{ 
  int i;
  for(i=4;i<=7;i++)
    pinMode(i, OUTPUT);  
  Serial.begin(9600);      //Set Baud Rate
  Serial.println("Run keyboard control");
} 
void loop(void) 
{
  back_off(255,255);
  delay(1000);
  stop();
  delay(1000);
}
