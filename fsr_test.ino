int fsrAnalogPin = 0; // FSR is connected to analog 0
int LEDpin = 11;      // connect Red LED to pin 11 (PWM pin)
int fsrReading;      // the analog reading from the FSR resistor divider
int fsrVoltage;
float fsrResistance;
int LEDbrightness;
 
void setup(void) {
  Serial.begin(9600);   // We'll send debugging information via the Serial monitor
  pinMode(LEDpin, OUTPUT);
}
 
void loop(void) {
  fsrReading = analogRead(fsrAnalogPin);
  fsrVoltage = map(fsrReading, 0, 1023, 0, 5000);
  // The voltage = Vcc * R / (R + FSR) where R = 180 and Vcc = 5V
  // so FSR = ((Vcc - V) * R) / V
  fsrResistance = 5000 - fsrVoltage;
  fsrResistance *= 180;       
  fsrResistance /= fsrVoltage;
  // Serial.print("FSR resistance in ohms = ");
  Serial.println(fsrResistance);
 
  delay(500);
}