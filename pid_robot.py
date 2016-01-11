
from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro, Motor


class PIDRobot(SyncedSketch):

    pins = 21, 22
    ss_pin = 10
    desired_angle = 90
    K_p = 3
    K_i = 2
    K_d = .25
    prevTime = 0
    currentTime = 0
    diff_prev = 0

    def setup(self):
        self.encoder_left = Encoder(self.tamp, 29,30, continuous=False)
        self.encoder_right = Encoder(self.tamp, 21, 22, continuous=False)
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        self.motor_left = Motor(self.tamp, 2, 3) #False is forwards; this is the left wheel
        self.motor_right = Motor(self.tamp, 8, 9) #True is forwards; this is the right wheel
        
        
        self.timer = Timer()
        self.prevTime = self.timer.millis()

    def loop(self):
        if self.timer.millis() > 50:
            self.currentTime = self.timer.millis()
            deltaT = (self.currentTime - self.prevTime) / 1000.0
            self.prevTime = self.currentTime
        
            self.timer.reset()
            
            self.prevTime = self.timer.millis()

            self.encoder_left.update()
            self.encoder_right.update()
            #print "Left encoder: " + str(self.encoder_left.val)
            #print "Right encoder: " + str(self.encoder_right.val)
            print "Gyro stuff: " + str(self.gyro.val) + " " + str(self.gyro.status)
            


            diff = self.desired_angle - self.gyro.val
            integral = 0
            derivative = 0
            print deltaT
            if(deltaT != 0):
                integral += diff * deltaT
                derivative = (diff - self.diff_prev)/deltaT

            P = diff * self.K_p
            D = derivative * self.K_d
            I = integral * self.K_i

            power = P + I + D

            print power
            self.motor_left.write(True, max(abs(50),50 + power))
            self.motor_right.write(True, max(abs(50), 50 - power))
            
            self.diff_prev = diff

if __name__ == "__main__":
    sketch = PIDRobot(1, -0.00001, 100)
    sketch.run()