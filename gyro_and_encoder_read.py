from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro


class GyroAndEncoderRead(SyncedSketch):

    pins = 21, 22
    ss_pin = 10

    def setup(self):
        self.encoder_left = Encoder(self.tamp, 29,30, continuous=False)
        self.encoder_right = Encoder(self.tamp, 21, 22, continuous=False)
        # self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 200:
            self.timer.reset()
            self.encoder_left.update()
            self.encoder_right.update()
            print "Left encoder: " + str(self.encoder_left.val)
            print "Right encoder: " + str(self.encoder_right.val)
            #print "Gyro stuff: " + str(self.gyro.val) + " " + str(self.gyro.status)
            #angle estimate from encoders calculated below
            # left_ticks = self.encoder_left.val
            # right_ticks = self.encoder_right.val
            
            # delta_left_ticks = left_ticks - self.last_left_ticks
            # delta_right_ticks = right_ticks - self.last_right_ticks
            
            # self.last_left_ticks = left_ticks
            # self.last_right_ticks = right_ticks

            # left_distance = (delta_left_ticks / self.CLICKS_PER_REV) * self.TWO_PI * self.WHEEL_RADIUS
            # right_distance = (delta_right_ticks / self.CLICKS_PER_REV) * self.TWO_PI * self.WHEEL_RADIUS

            # distance_traveled = (left_distance + right_distance) / 2.0
            # theta_encoder = (left_distance - right_distance) / self.WHEEL_BASE
            # theta_encoder *= 180 / math.pi

            # x_change = distance_traveled * math.cos(theta_encoder)

            # y_change = distance_traveled * math.sin(theta_encoder)

            # self.filtered_angle = (self.filtered_angle + self.gyro.val) * .9 + theta_encoder * .1
            

if __name__ == "__main__":
    sketch = GyroAndEncoderRead(1, -0.00001, 100)
    sketch.run()