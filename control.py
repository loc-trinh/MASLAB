
from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro, Motor


class PIDRobot(SyncedSketch):

    pins = 21, 22
    ss_pin = 10
    desired_angle = 0
    K_p = 3
    K_i = 2
    K_d = -.25
    last_diff = 0
    integral = 0
    dT = 50/1000.
    runtime = 8000

    def setup(self):
        self.encoder_left = Encoder(self.tamp, 29,30, continuous=False)
        self.encoder_right = Encoder(self.tamp, 21, 22, continuous=False)
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        self.motor_left = Motor(self.tamp, 2, 3)
        self.motor_right = Motor(self.tamp, 8, 9)
        self.timer = Timer()
        self.stop_timer = Timer()

    def loop(self):
        if self.stop_timer.millis() > self.runtime:
            self.stop()
        if self.timer.millis() > 50:
            self.timer.reset()
            self.encoder_left.update()
            self.encoder_right.update()

            diff = self.desired_angle - self.gyro.val
            self.integral += diff * self.dT
            derivative = float(self.last_diff - diff)/self.dT
            power = self.K_p*diff + self.K_i*self.integral + self.K_d*derivative
            self.last_diff = diff

            self.motor_left.write(True, max(20,50 + power))
            self.motor_right.write(True, max(20, 50 - power))

    def stop(self):
        super(PIDRobot,self).stop()
        self.tamp.clear_devices();


if __name__ == "__main__":
    sketch = PIDRobot(1, -0.00001, 100)
    sketch.run()