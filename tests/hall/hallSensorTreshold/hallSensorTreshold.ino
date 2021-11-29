int  count;
void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  count=0;
}

void loop() {
  int hall = analogRead(A0);
  boolean near = (hall < 500 || hall > 550);
  if(near){
  while(near){
    near = (hall < 500 || hall > 550);
  }
  count++;  
  digitalWrite(2, 1);
  Serial.println(count);
  }
}
