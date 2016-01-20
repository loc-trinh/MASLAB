from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro


class EncoderRead(SyncedSketch):
    ss_pin = 10

    def setup(self):
        self.encoder_left = Encoder(self.tamp, 29,30, continuous=False)
        self.encoder_right = Encoder(self.tamp, 19, 20, continuous=False)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 200:
            self.timer.reset()
            self.encoder_left.update()
            self.encoder_right.update()
            print "Left encoder: " + str(self.encoder_left.val)
            print "Right encoder: " + str(self.encoder_right.val)

if __name__ == "__main__":
    sketch = EncoderRead(1, -0.00001, 100)
    sketch.run()