from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Motor

# Cycles a motor back and forth between -255 and 255 PWM every ~5 seconds

class WallFollower(Sketch):

    def setup(self):
        self.motor = Motor(self.tamp, 2, 3) #False is forwards; this is the left wheel
        self.motor2 = Motor(self.tamp, 8, 9) #True is forwards; this is the right wheel
        self.motor.write(1,0)
        self.delta = 1
        self.motorval = 0
        #CHANGE THE TWO SENSOR INPUTS BELOW UNTIL PINS ARE VALID
        self.sensor_right_front = AnalogInput(self.tamp, 28)
        self.sensor_right_back = AnalogInput(self.tamp,27)
        self.sensor_front_center = AnalogInput(self.tamp,26)
        self.K = 15
        self.timer = Timer()

        
    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            center_reading = self.convertToInches(self.sensor_front_center.val)
            front_reading = self.convertToInches(self.sensor_right_front.val)
            back_reading = self.convertToInches(self.sensor_right_back.val)
            if(center_reading < 8.0):
                #something is in front; turn left
                self.motor.write(False, abs(100))
                self.motor2.write(True, abs(100))
            else:
                front_minus_back = front_reading - back_reading
                #if(front_minus_back > 0 and abs(front_minus_back) > 1.5):
                    #favor the left side a bit more
                self.motor_left.write(True, max(abs(20),50 + (self.K * front_minus_back)))
                self.motor_right.write(True, max(abs(20), 50 - (self.K * front_minus_back)))
            #     elif(front_minus_back < 0 and abs(front_minus_back) > 1.5):
            #         #favor the right side a bit more
            #         self.motor_left.write(True, max(abs(50),50 - (self.K * diff)))
            # self.motor_right.write(True, max(abs(50), 50 + (self.K * diff)))
            #     else:
            #         #not enough of a difference; go straight
            #         self.motor.write(True, abs(100))
            #         self.motor2.write(True, abs(100))

    def convertToInches(self, value):
        return -7.87402 * ln(value * .00001506809)
        #return -.127 * ln(value / 66362.0)
if __name__ == "__main__":
    sketch = WallFollower()
    sketch.run()
