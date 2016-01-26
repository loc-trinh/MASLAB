from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Color, Servo, Motor, Encoder
from random import randint

# Prints RGB, clear(C), colorTemp, and lux values read and
# computed from the device. For more details, see the Adafruit_TCS34725
# Arduino library, from which the colorTemp and lux computations are
# used.

# Color sensor should be connected to the I2C ports (SDA and SCL)

#CENTER IS 53
#RIGHT WAS 27

class SortBlocks(SyncedSketch):

    pins = 31, 32

    def setup(self):
        self.LEFT_TOWER = 85
        self.RIGHT_TOWER = 24
        self.CENTER = 53


        self.color = Color(self.tamp,
                           integrationTime=Color.INTEGRATION_TIME_101MS,
                           gain=Color.GAIN_1X)
        self.servo = Servo(self.tamp, 23) #pin TBD
        self.red_detected = False
        self.green_detected = False
        self.servo.write(self.CENTER)
        self.counter = 0
        self.servo_bottom = Servo(self.tamp,22)
        self.servo_bottom.write(34)

        self.motor = Motor(self.tamp, 24, 25)
        self.motor.write(True, 250)
        self.jammed = False

        self.conveyor_encoder = Encoder(self.tamp, *self.pins, continuous=True)
        self.prev_encoder_value = 0
        self.conveyor_encoder.update()
        self.timer = Timer()

        self.sorter_delta = 50
        
    def loop(self):
        if self.timer.millis() > 300:
            self.timer.reset()
            #self.conveyor_encoder.update()
            encoder_value = self.conveyor_encoder.val
            #print self.prev_encoder_value
            #print encoder_value
            if(encoder_value == self.prev_encoder_value):
                self.jammed = True
            else:
                self.jammed = False
            self.prev_encoder_value = encoder_value
            self.motor.write(not self.jammed,250)

            # print self.color.r, self.color.g, self.color.b, self.color.c
            # print self.color.colorTemp, self.color.lux
            #if not self.red_detected and not self.green_detected and self.color.r > 1.3 * self.color.g and self.color.r > 1.3 * self.color.b:
            detect_red = self.color.r > 1.3*self.color.g
            detect_green = self.color.g > 1.3*self.color.r
            sum_val = self.color.r+self.color.g+self.color.b
            if detect_red and sum_val > 300:
                self.servo.write(self.LEFT_TOWER)
                self.counter = 0
            #elif not self.red_detected and not self.green_detected and self.color.g > 1.3 * self.color.r and self.color.g > 1.3 * self.color.b:
            elif detect_green and sum_val > 300:
                self.servo.write(self.RIGHT_TOWER)
                self.counter = 0
            elif self.counter > 400:
                self.servo.write(self.CENTER)
            # else:
            #     self.servo.write(self.CENTER + self.sorter_delta)
            #     self.sorter_delta *= -1
            self.counter += 100

if __name__ == "__main__":
    sketch = SortBlocks(1, -0.00001, 100)
    sketch.run()
