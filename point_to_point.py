
from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro, Motor
import math

class PointToPointRobot(SyncedSketch):

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
    last_left_ticks = 0
    last_right_ticks = 0
    CLICKS_PER_REV = 3200
    TWO_PI = math.pi * 2.0
    WHEEL_BASE = 11.5 #inches
    WHEEL_RADIUS = 2.0 #inches

    x_pos = 0
    y_pos = 0

    threshold = .1

    points = [(1,0),(1,1),(0,1),(0,0)]
    CURRENT_POINT_INDEX = 0

    def setup(self):
        self.encoder_left = Encoder(self.tamp, 29,30, continuous=False)
        self.encoder_right = Encoder(self.tamp, 21, 22, continuous=False)
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        self.motor_left = Motor(self.tamp, 2, 3)
        self.motor_right = Motor(self.tamp, 8, 9)
        self.timer = Timer()
        self.stop_timer = Timer()
        self.filtered_angle = 0

    def loop(self):
        if self.timer.millis() > 50:
            self.timer.reset()
            self.encoder_left.update()
            self.encoder_right.update()

            #update point if necessary
            if(abs(self.x_pos - self.points[CURRENT_POINT_INDEX][0]) < self.threshold and abs(self.y_pos - self.points[CURRENT_POINT_INDEX][1]) < self.threshold):
                CURRENT_POINT_INDEX += 1
            if(CURRENT_POINT_INDEX >= 4):
                return

            #calculate desired angle
            self.desired_angle = math.atan2(self.points[CURRENT_POINT_INDEX][0] - self.x_pos,self.points[CURRENT_POINT_INDEX][1] - self.y_pos)
            self.desired_angle *= 180.0 / math.pi

            

            #angle estimate from encoders calculated below
            left_ticks = self.encoder_left.val
            right_ticks = self.encoder_right.val
            
            delta_left_ticks = left_ticks - self.last_left_ticks
            delta_right_ticks = right_ticks - self.last_right_ticks
            
            self.last_left_ticks = left_ticks
            self.last_right_ticks = right_ticks

            left_distance = (delta_left_ticks / self.CLICKS_PER_REV) * self.TWO_PI * self.WHEEL_RADIUS
            right_distance = (delta_right_ticks / self.CLICKS_PER_REV) * self.TWO_PI * self.WHEEL_RADIUS

            distance_traveled = (left_distance + right_distance) / 2.0
            theta_encoder = (left_distance - right_distance) / self.WHEEL_BASE
            #theta_encoder *= 180 / math.pi

            
            self.filtered_angle = (self.filtered_angle + self.gyro.val) * .9 + (theta_encoder * 180.0 / math.pi) * .1

            x_change = distance_traveled / 24.0 * math.cos(filtered_angle)

            y_change = distance_traveled / 24.0 * math.sin(filtered_angle)
            #division by 24 to account for fact that 1 unit in map space corresponds to 2 ft in real space (and units are currently in inches)

            self.x_pos += x_change
            self.y_pos += y_change

            diff = self.desired_angle - self.filtered_angle

            if(diff > 180):
                while(diff > 180):
                    diff -= 360
            elif(diff < -180):
                while(diff < -180):
                    diff += 360

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
    sketch = PointToPointRobot(1, -0.00001, 100)
    sketch.run()