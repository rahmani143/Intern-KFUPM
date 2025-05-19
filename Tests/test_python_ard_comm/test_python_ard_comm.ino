// int number1;
// String receivedstring;
// String sendbackinteger;

// void setup() {
//   // put your setup code here, to run once:
//   Serial.begin(9600);
// }

// void loop() {
//   // put your main code here, to run repeatedly:
//   while(Serial.available() == 0)
  
//   receivedstring = Serial.readString();

//   number1 = receivedstring.toInt();

//   number1 = number1+ 100;

//   sendbackinteger = String(number1);

//   Serial.print(sendbackinteger);
// }

void setup()
{
    Serial.begin(9600);
    Serial.setTimeout(1);
}

void loop()
{
    String message;
    while(!Serial.available());
    message = Serial.readString();
    message.toUpperCase();
    Serial.print(message);
}


