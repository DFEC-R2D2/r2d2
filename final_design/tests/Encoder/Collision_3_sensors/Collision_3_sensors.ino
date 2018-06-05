// Sharp IR GP2Y0A41SK0F Distance Test
// http://tinkcore.com/sharp-ir-gp2y0a41-skf/

#define sensor A0 // Sharp IR GP2Y0A41SK0F (4-30cm, analog)

int trigPin = 9;    //Trig - green Jumper
int echoPin = 10;    //Echo - yellow Jumper
int trigPin2 = 11;
int echoPin2 = 12;
long duration, cm, inches;
long duration2, cm2, inches2;


void setup() {
  Serial.begin(9600); // start the serial port

    //Define inputs and outputs
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
}

void loop() {
  if (Serial.available()){
    int d = Serial.read()-'0';
      while ( d == 1 )
      {
         // IR Sensor 1
        float volts = analogRead(sensor)*0.0048828125;  // value from sensor * (5/1024)
        int distance = 13*pow(volts, -1); // worked out from datasheet graph
//        delay(500); // slow down serial port 
        Serial.println(distance/2);   // print the distance

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

      Serial.println(cm);
      
      delay(300);
  
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
    
      Serial.println(cm2);
      }
  }
}
