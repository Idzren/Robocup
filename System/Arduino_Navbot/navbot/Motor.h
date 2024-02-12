// Motor.h - Library for controlling motors with Arduino.
#ifndef Motor_h
#define Motor_h

#include "Arduino.h"

class Motor {
public:
    Motor(int plus, int minus, int en_a, int en_b); // Constructor
    void rotate(int value); // Method to control motor speed and direction

private:
    int plus, minus; // Motor control pins for direction
    int en_a, en_b;  // Encoder pins for feedback

    void setupPins(); // Private method to setup pin modes
};

#endif
