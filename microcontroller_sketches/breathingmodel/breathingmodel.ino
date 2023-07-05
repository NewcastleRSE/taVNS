#define DAC_CH1 25

float P[] = { 1.581, -5.534, 0.5523 };
float w[] = { 1.214, 0.001414, 2.401 };
float c[] = { -0.3132, 3.297, -2.381 };

float R[] = { 1.137, 1.137 };
float C[] = { 0.1066, 0.0533 };
float tao[2][2] = { { 2.115, 0.5289 }, { 0.2198, 1.0320 } };
float t = 0;
int maxval = 0;
int minval = 0;

void setup() {
  Serial.begin(9600);

}

void loop() {
  int result = twocomplinear(t);
  int dacout = normalise(result, -100, 1000);
  dacWrite(DAC_CH1, dacout);
  Serial.println(dacout);
  t += 0.1;
  if (t > 5) {
    t = 0;
  }
  delay(100);
}

int twocomplinear(float t) {
  float result = 0;
  for (int i = 0; i < 3; i++) {
    for (int lung = 0; lung < 2; lung++) {
      result += P[i] * C[lung] * (sin(w[i] * t + c[i]) - w[i] * (sq(R[lung] * C[lung]) * cos(w[i] * t + c[i])) / (1 + w[i] * w[i] * (sq(R[lung] * C[lung]))));
    }
  }
  return (int)(result * 1000);
}

int normalise(int x, int xmin, int xmax) {
  int a = 0;
  int b = 256;
  return a + (((x - xmin) * (b - a)) / (xmax - xmin));
}