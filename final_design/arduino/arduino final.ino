//Ultrasonic 1 Initialization
int trigPin = 2;
int echoPin = 3;

//Ultrasonic 2 Initialization
int trigPin2 = 4;   
int echoPin2 = 5;

//Ultrasonic 3 Initialization
int trigPin3 = 6;
int echoPin3 = 7;

//Ultrasonic 4 Initialization
int trigPin4 = 8;
int echoPin4 = 9;

//Variable Initialization
long duration, cm, inches;
long duration2, cm2, inches2;
long duration3, cm3, inches3;
long duration4, cm4, inches4;

//Battery Reading Ports Initialization
int analogPin = A3;     // potentiometer wiper (middle terminal) connected to analog pin 3
int val = 0;           // variable to store the value read

void setup() {
  Serial.begin(19200); // start the serial port

  //Ultrasonic 1 IO
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  //Ultrasonic 2 IO
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  
  //Ultrasonic 3 IO
  pinMode(trigPin3, OUTPUT);
  pinMode(echoPin3, INPUT);
  
  //Ultrasonic 4 IO
  pinMode(trigPin4, OUTPUT);
  pinMode(echoPin4, INPUT);
}

void loop() {
if (Serial.available()){
      int d = Serial.read()-'0';
      if ( d == 2 )
      {
      // Read Battery and LED
      val = analogRead(analogPin);     // read the input pin
      float voltage = val * (5.0 / 1023.0);
      Serial.println(voltage);      
      }
      
      if ( d == 1 )
      {
      // Ultrasonic Sensor 1
      // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
      // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
      digitalWrite(trigPin, LOW);
      delayMicroseconds(5);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);
 
      // Read the signal from the sensor: a HIGH pulse whose
      // duration is the time (in microseconds) from the sending
      // of the ping to the reception of its echo off of an object.
      pinMode(echoPin, INPUT);
      duration = pulseIn(echoPin, HIGH);
 
      // convert the time into a distance
      cm = (duration/2) / 29.1;
      inches = (duration/2) / 74; 
  
      // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
      // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
      digitalWrite(trigPin2, LOW);
      delayMicroseconds(5);
      digitalWrite(trigPin2, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin2, LOW);
 
      // Read the signal from the sensor: a HIGH pulse whose
      // duration is the time (in microseconds) from the sending
      // of the ping to the reception of its echo off of an object.
      pinMode(echoPin2, INPUT);
      duration2 = pulseIn(echoPin2, HIGH);
     
      // convert the time into a distance
      cm2 = (duration2/2) / 29.1;
      inches2 = (duration2/2) / 74; 
  
      // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
      // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
      digitalWrite(trigPin3, LOW);
      delayMicroseconds(5);
      digitalWrite(trigPin3, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin3, LOW);
 
      // Read the signal from the sensor: a HIGH pulse whose
      // duration is the time (in microseconds) from the sending
      // of the ping to the reception of its echo off of an object.
      pinMode(echoPin3, INPUT);
      duration3 = pulseIn(echoPin3, HIGH);
     
      // convert the time into a distance
      cm3 = (duration3/2) / 29.1;
      inches3 = (duration3/2) / 74; 
      
      // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
      // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
      digitalWrite(trigPin4, LOW);
      delayMicroseconds(5);
      digitalWrite(trigPin4, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin4, LOW);
 
      // Read the signal from the sensor: a HIGH pulse whose
      // duration is the time (in microseconds) from the sending
      // of the ping to the reception of its echo off of an object.
      pinMode(echoPin4, INPUT);
      duration4 = pulseIn(echoPin4, HIGH);
     
      // convert the time into a distance
      cm4 = (duration4/2) / 29.1;
      inches4 = (duration4/2) / 74; 

      Serial.println(cm);
      Serial.println(cm2);
      Serial.println(cm3);
      Serial.println(cm4);
      }
  }
}
