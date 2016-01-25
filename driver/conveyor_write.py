from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Motor

# Cycles a motor back and forth between -255 and 255 PWM every ~5 seconds

class MotorWrite(Sketch):

    def setup(self):
        self.motor = Motor(self.tamp, 24, 25)
        self.motor.write(1,0)
        self.delta = 1
        self.motorval = 0
        self.timer = Timer()
        self.counter = 0
        self.spin_forwards = True
    def loop(self):
        if (self.timer.millis() > 10):
            self.timer.reset()
            # if abs(self.motorval) == 255: self.delta = -self.delta
            #     self.motorval += self.delta
            #     self.motor.write(self.motorval>0, abs(self.motorval))
            if(self.counter >= 2000 and self.spin_forwards):
                self.counter = 0
                self.spin_forwards = False
            elif(self.counter >= 500 and not self.spin_forwards):
                self.counter = 0
                self.spin_forwards = True
            self.motor.write(self.spin_forwards, 250)
            self.counter += 10

if __name__ == "__main__":
    sketch = MotorWrite()
    sketch.run()