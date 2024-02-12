#include "Motor.h"
#include <ros.h>
#include <geometry_msgs/Twist.h>

ros::NodeHandle nh;

Motor rightMotor(6, 7, 2, 3); // Right motor connected to pins 6, 7 for control and 2, 3 for encoders
Motor leftMotor(4, 5, 18, 19); // Left motor connected to pins 4, 5 for control and 18, 19 for encoders

void cmdVelCallback(const geometry_msgs::Twist& cmd_vel){
    float linear = cmd_vel.linear.x; // Linear velocity in m/s
    float angular = cmd_vel.angular.z; // Angular velocity in rad/s

    // Simple differential drive robot model for demonstration
    // Assumes a fixed robot width and maps linear & angular speed to motor speeds
    int leftSpeed = (linear - angular * 0.1) * 100; // Scale factors for demonstration
    int rightSpeed = (linear + angular * 0.1) * 100;

    // Control motors with calculated speeds
    leftMotor.rotate(leftSpeed);
    rightMotor.rotate(rightSpeed);
}

ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", cmdVelCallback);

void setup() {
  nh.initNode();
  nh.subscribe(sub);
}

void loop() {
  nh.spinOnce(); // Handle ROS callbacks
  delay(10); // Small delay to prevent spinning too fast
}
