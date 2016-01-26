from driver.tamproxy import SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro, Motor, AnalogInput, Color, Servo
import random
import zmq
from math import log as ln

class IRBot(SyncedSketch):
    def setup(self):
        # =============== IR setup ================= #
        self.left_front = AnalogInput(self.tamp, 10)
        self.left_side = AnalogInput(self.tamp, 11)
        self.right_front = AnalogInput(self.tamp, 12)
        self.right_side = AnalogInput(self.tamp, 13)
        self.timer = Timer()
        

    def loop(self):
        if self.timer.millis() > 300:
            self.timer.reset()
            lf = self.convertToInches(self.left_front.val)
            ls = self.convertToInches(self.left_side.val)
            rf = self.convertToInches(self.right_front.val)
            rs = self.convertToInches(self.right_side.val)
            print ls, lf, rf, rs



    def convertToInches(self, value):
        inches = 0 if value <= 0 else -5.07243 * ln(0.0000185668 * value)
        return inches


if __name__ == "__main__":
    sketch = IRBot(1, -0.00001, 100)
    sketch.run()
