/* General info:
 * this code works for ---> analog joysticks <----!
 * hold the joy stick so you can read the pin describtion correctly,
 * we have to invert y pin to feel more natural!
 * and we want the idle pos. to be (0, 0) so fetch the idle coordinates on setup()
  
 * Coordinates:
 * y ^ 
 *   |
 *   |
 * (0,0) - - > x
*/

// arduino pin numbers
const int SW_pin = 7; // digital pin connected to switch output
const int X_pin = A0; // analog pin connected to X output
const int Y_pin = A1; // analog pin connected to Y output

// idle position x, y of the joy stick
int x0, y0;

// previous coordinates
int prevX, prevY;
// noise threshold
const int threshold = 1;

// current coordinates
int x, y;


int readX(const int pin, int x0) {
  return(analogRead(pin) - x0);
}

int readY(const int pin, int y0) {
  return(map(analogRead(pin), 0, 1023, 1023, 0) - y0);
}

// to cancel the small noise (+/- 1 while holding still)
boolean has_really_changed(int val, int prev) {
  return( ((val-prev)*(val-prev) <= threshold) ? false : true );
}

// for deugging purpose only
void printAll() {
  Serial.println("------- debugging info: -------");
  Serial.println("prevX=" + String(prevX) + ", prevY=" + String(prevY));
  Serial.println("x=" + String(x) + ", y=" + String(y));
}

void setup() {
  // for the press functionallity we set the switch pin to
  // internal pull up resistor => +5V level if not pressed, 0V if pressed! 
  // fetch status with: int status = digitalRead(SW_pin);
  pinMode(SW_pin, INPUT);
  digitalWrite(SW_pin, HIGH);
  
  Serial.begin(9600);
  
  // fetch the idle position
  x0 = analogRead(X_pin);
  y0 = map(analogRead(Y_pin), 0, 1023, 1023, 0);
  
  // initialize prev values for noise canceling
  prevX = 0;
  prevY = 0;
}

void loop() {
  // read coordinates with noise
  x = readX(X_pin, x0);
  y = readY(Y_pin, y0);
  
  // print coordinates without noise
  // to reduce the load on the serial port by only printing coords
  // when they have really changed
  if(has_really_changed(x, prevX)) {
    Serial.println("x=" + String(x));
  }
  if(has_really_changed(y, prevY)) {
    Serial.println("y=" + String(y));
  }

  // save current values, which will e the previous ones on next iteration
  prevX = x;
  prevY = y;

  delay(1);
}
