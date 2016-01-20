from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Motor, Encoder

class MotorWrite(Sketch):

    def setup(self):
        self.motor = Motor(self.tamp, 2, 3)
        self.motor2 = Motor(self.tamp, 8, 9)

        self.motor.write(1,0)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            self.motor.write(True, abs(50))
            self.motor2.write(True, abs(50))


if __name__ == "__main__":
    sketch = MotorWrite()
    sketch.run()
