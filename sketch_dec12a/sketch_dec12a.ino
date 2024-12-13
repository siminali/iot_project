const int LED_PIN = 5;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600); // Start serial communication
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readString(); // Read data from serial

    if (data == "HIGH") {
      digitalWrite(LED_PIN, HIGH); // Turn on LED
    } else if (data == "LOW") {
      digitalWrite(LED_PIN, LOW); // Turn off LED
    }
  }
}
