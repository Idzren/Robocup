#include "Motor.h"

Motor::Motor(int plus, int minus, int en_a, int en_b) {
    this->plus = plus;
    this->minus = minus;
    this->en_a = en_a;
    this->en_b = en_b;
    setupPins();
}

void Motor::rotate(int value) {
    // Assuming value range is -100 to 100
    if (value >= 0) {
        int out = map(value, 0, 100, 0, 255); // Adjust PWM mapping as needed
        analogWrite(plus, out);
        analogWrite(minus, 0);
    } else {
        int out = map(value, -100, 0, 255, 0);
        analogWrite(plus, 0);
        analogWrite(minus, out);
    }
}

void Motor::setupPins() {
    pinMode(plus, OUTPUT);
    pinMode(minus, OUTPUT);
    // Encoder pins are set as INPUT_PULLUP if they're used for interrupts
    pinMode(en_a, INPUT_PULLUP);
    pinMode(en_b, INPUT_PULLUP);
}
