from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro


class GyroAndEncoderRead(SyncedSketch):
    ss_pin = 10

    def setup(self):
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        self.timer = Timer()
        self.gyro_balancer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print "Gyro stuff: " + str(self.gyro.val) + " " + str(self.gyro.status)

if __name__ == "__main__":
    sketch = GyroAndEncoderRead(1, -0.00001, 100)
    sketch.run()