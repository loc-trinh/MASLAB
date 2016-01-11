
from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro, Motor


class DrunkRobot(SyncedSketch):

    pins = 21, 22
    ss_pin = 10
    desired_angle = 0
    K = 3

    def setup(self):
        self.encoder_left = Encoder(self.tamp, 29,30, continuous=False)
        self.encoder_right = Encoder(self.tamp, 21, 22, continuous=False)
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        self.motor_left = Motor(self.tamp, 2, 3) #False is forwards; this is the left wheel
        self.motor_right = Motor(self.tamp, 8, 9) #True is forwards; this is the right wheel
        
        
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            #print "here"
            self.encoder_left.update()
            self.encoder_right.update()
            #print "Left encoder: " + str(self.encoder_left.val)
            #print "Right encoder: " + str(self.encoder_right.val)
            #print "Gyro stuff: " + str(self.gyro.val) + " " + str(self.gyro.status)
            diff = self.desired_angle - self.gyro.val
            self.motor_left.write(True, max(abs(50),50 + (self.K * diff)))
            self.motor_right.write(True, max(abs(50), 50 - (self.K * diff)))
            

if __name__ == "__main__":
    sketch = DrunkRobot(1, -0.00001, 100)
    sketch.run()