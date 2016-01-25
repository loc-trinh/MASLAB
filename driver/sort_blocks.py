from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Color, Servo

# Prints RGB, clear(C), colorTemp, and lux values read and
# computed from the device. For more details, see the Adafruit_TCS34725
# Arduino library, from which the colorTemp and lux computations are
# used.

# Color sensor should be connected to the I2C ports (SDA and SCL)

#CENTER IS 54

class SortBlocks(SyncedSketch):

    def setup(self):
        self.LEFT_TOWER = 83.4
        self.RIGHT_TOWER = 27
        self.CENTER = 54


        self.color = Color(self.tamp,
                           integrationTime=Color.INTEGRATION_TIME_101MS,
                           gain=Color.GAIN_1X)
        self.servo = Servo(self.tamp, 23) #pin TBD
        self.red_detected = False
        self.green_detected = False
        self.servo.write(self.CENTER)
        self.counter = 0
        self.timer = Timer()

        
    def loop(self):
        if self.timer.millis() > 200:
            self.timer.reset()
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
            self.counter += 100

if __name__ == "__main__":
    sketch = SortBlocks(1, -0.00001, 100)
    sketch.run()
