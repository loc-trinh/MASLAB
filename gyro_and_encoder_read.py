
from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro


class GyroAndEncoderRead(SyncedSketch):

    pins = 21, 22
    ss_pin = 10


    def setup(self):
        self.encoder_left = Encoder(self.tamp, 29,30, continuous=False)
        self.encoder_right = Encoder(self.tamp, 21, 22, continuous=False)
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print "here"
            self.encoder_left.update()
            self.encoder_right.update()
            print "Left encoder: " + str(self.encoder_left.val)
            print "Right encoder: " + str(self.encoder_right.val)
            print "Gyro stuff: " + str(self.gyro.val) + " " + str(self.gyro.status)
            

if __name__ == "__main__":
    sketch = GyroAndEncoderRead(1, -0.00001, 100)
    sketch.run()