
from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro, Motor, AnalogInput

import math
from random import randint
from math import log as ln

class PIDRobot(SyncedSketch):

    pins = 21, 22
    ss_pin = 10
    desired_angle = 0
    K_p = .5
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

    LINE_TIME = 2000
    counter = 0
    FRONT_DISTANCE_THRESHOLD = 8
    SIDE_DISTANCE_THRESHOLD = 4
    #angle between -180 and 180

    left_front_pin = 10
    left_side_pin = 11
    right_front_pin = 12
    right_side_pin = 13

    prev_values_lf = []
    prev_values_ls = []
    prev_values_rf = []
    prev_values_rs = []

    sensor_reading_counter = 0

    def setup(self):
        self.encoder_left = Encoder(self.tamp, 29,30, continuous=False)
        self.encoder_right = Encoder(self.tamp, 16, 17, continuous=False)
        self.gyro = Gyro(self.tamp, 10, integrate=True)
        self.motor_left = Motor(self.tamp, 2, 3)
        self.motor_right = Motor(self.tamp, 8, 9)
        self.timer = Timer()
        self.stop_timer = Timer()
        self.filtered_angle = 0

        self.left_front = AnalogInput(self.tamp, self.left_front_pin)
        self.left_side = AnalogInput(self.tamp, self.left_side_pin)
        self.right_front = AnalogInput(self.tamp, self.right_front_pin)
        self.right_side = AnalogInput(self.tamp, self.right_side_pin)


    def loop(self):
        # if self.stop_timer.millis() > self.runtime:
        #     self.stop()
        if self.timer.millis() > 50:
            self.timer.reset()
            self.encoder_left.update()
            self.encoder_right.update()

            if(self.sensor_reading_counter <= 10):
                self.prev_values_lf.append(self.convertToInches(self.left_front.val))
                self.prev_values_ls.append(self.convertToInches(self.left_side.val))
                self.prev_values_rf.append(self.convertToInches(self.right_front.val))
                self.prev_values_rs.append(self.convertToInches(self.right_side.val))
                self.sensor_reading_counter += 1

            else:
                self.prev_values_lf[self.counter % 10] = self.convertToInches(self.left_front.val)
                self.prev_values_ls[self.counter % 10] = self.convertToInches(self.left_side.val)
                self.prev_values_rf[self.counter % 10] = self.convertToInches(self.right_front.val)
                self.prev_values_rs[self.counter % 10] = self.convertToInches(self.right_side.val)
                self.sensor_reading_counter += 1

            average_lf_value = sum(self.prev_values_lf) / len(self.prev_values_lf)
            average_ls_value = sum(self.prev_values_ls) / len(self.prev_values_ls)
            average_rf_value = sum(self.prev_values_rf) / len(self.prev_values_rf)
            average_rs_value = sum(self.prev_values_rs) / len(self.prev_values_rs)

            #angle estimate from encoders calculated below
            left_ticks = -self.encoder_left.val
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

            x_change = distance_traveled * math.cos(self.filtered_angle)

            y_change = distance_traveled * math.sin(self.filtered_angle)
            print "desired_angle: " + str(self.desired_angle)
            print "gyro_val: " + str(self.gyro.val)
            print "average_lf_value: " + str(average_lf_value)
            print "average_ls_value: " + str(average_ls_value)
            print "average_rf_value: " + str(average_rf_value)
            print "average_rs_value: " + str(average_rs_value)


            if(self.counter >= self.LINE_TIME or average_lf_value < self.FRONT_DISTANCE_THRESHOLD or average_rf_value < self.FRONT_DISTANCE_THRESHOLD 
                or average_ls_value < self.SIDE_DISTANCE_THRESHOLD or average_rs_value < self.SIDE_DISTANCE_THRESHOLD):
                self.counter = 0
                self.desired_angle = randint(-180,180)
                self.LINE_TIME = randint(2,5) * 1000

            # elif(average_lf_value < FRONT_DISTANCE_THRESHOLD):
            #     self.counter = 0
            #     self.desired_angle = randint()
            # elif(average_ls_value < SIDE_DISTANCE_THRESHOLD):

            # elif(average_rf_value < FRONT_DISTANCE_THRESHOLD):

            # elif(average_rs_value < SIDE_DISTANCE_THRESHOLD):


            diff = self.desired_angle - self.gyro.val
            self.integral += diff * self.dT
            derivative = float(self.last_diff - diff)/self.dT
            power = self.K_p*diff + self.K_i*self.integral + self.K_d*derivative
            self.last_diff = diff

            self.motor_left.write(True, max(0,20 + power))
            self.motor_right.write(True, max(0,20 - power))

            self.counter += 50

    def stop(self):
        super(PIDRobot,self).stop()
        self.tamp.clear_devices();

    def convertToInches(self, value):
        '''MID RANGE MODEL'''
        #first model:
        #return -5.47336 * ln(0.0000197638 * value)
        #second model:
        if value <= 0:
            return 0
        return -5.07243 * ln(0.0000185668 * value)

if __name__ == "__main__":
    sketch = PIDRobot(1, -0.00001, 100)
    sketch.run()