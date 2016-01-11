from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Motor

# Cycles a motor back and forth between -255 and 255 PWM every ~5 seconds

class MotorWrite(Sketch):

    def setup(self):
        self.motor = Motor(self.tamp, 2, 3) #False is forwards; this is the left wheel
        self.motor2 = Motor(self.tamp, 8, 9) #True is forwards; this is the right wheel
        self.motor.write(1,0)
        self.delta = 1
        self.motorval = 0
        self.timer = Timer()

    def loop(self):
        self.motor.write(True, abs(100))
        self.motor2.write(True, abs(100))
if __name__ == "__main__":
    sketch = MotorWrite()
    sketch.run()
