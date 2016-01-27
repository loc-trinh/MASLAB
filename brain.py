from driver.tamproxy import SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro, Motor, AnalogInput, Color, Servo
import random
import zmq
from math import log as ln


class PID:
    def __init__(self, dT):
        self.Kp = 3
        self.Ki = .5
        self.Kd = -.3
        self.last_diff = 0
        self.integral = 0
        self.dT = dT

    def power(self, diff):
        self.integral += diff * self.dT
        derivative = float(self.last_diff - diff) / self.dT
        power = self.Kp * diff + self.Ki * self.integral + self.Kd * derivative
        self.last_diff = diff
        return power


class RandomBot(SyncedSketch):
    def setup(self):
        # =============== Encoder setup =============== #
        self.encoder_left = Encoder(self.tamp, 29, 30, continuous=False)
        self.encoder_right = Encoder(self.tamp, 19, 20, continuous=False)

        # =============== IR setup ================= #
        self.left_front = AnalogInput(self.tamp, 10)
        self.left_side = AnalogInput(self.tamp, 11)
        self.right_front = AnalogInput(self.tamp, 12)
        self.right_side = AnalogInput(self.tamp, 13)
        self.run_timer = Timer()
        self.RUN_TIME = 2000

        # =============== Gyro setup =============== #
        self.gyro = Gyro(self.tamp, 10, integrate=True)

        # =============== Motor setup =============== #
        self.motor_left = Motor(self.tamp, 2, 3)
        self.motor_right = Motor(self.tamp, 8, 9)

        # =============== Timer setup =============== #
        self.timer = Timer()
        self.INTERVAL = 30         # 30ms ~ 33.3 hz

        # =============== PID setup =============== #
        self.PID_controller = PID(self.INTERVAL / 1000.)
        self.desired_center = 80
        self.desired_angle = 0

        # =============== Vision setup ============= #
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")

        # ============ Sorting setup ============ #
        self.LEFT_TOWER = 85
        self.RIGHT_TOWER = 24
        self.CENTER = 53

        self.color = Color(self.tamp,
                           integrationTime=Color.INTEGRATION_TIME_101MS,
                           gain=Color.GAIN_1X)
        self.servo = Servo(self.tamp, 23)
        self.servo.write(self.CENTER+5)
        self.servo_val = self.CENTER-5

        self.servo_bottom = Servo(self.tamp,22)
        #self.servo_bottom.write(34)
        self.servo_bottom.write(90)
        self.second_timer = Timer()

        # ============== Intake setup ============ #
        self.motor = Motor(self.tamp, 24, 25)
        self.motor.write(True, 250)

        self.conveyor_encoder = Encoder(self.tamp, 32,32, continuous=True)
        self.conveyor_encoder.update()
        self.prev_encoder_value = 0
        self.third_timer = Timer()
        
        self.time_out = Timer()
        self.STOP = False

        self.conveyor_counter = 0

    def loop(self):
        if self.STOP:
            self.motor_left.write(True, 0)
            self.motor_right.write(True, 0)
            return
        #print self.third_timer.millis()
        if self.third_timer.millis() > 200:# and self.third_timer.millis() < 1400:
            self.motor.write(True,250)
            encoder_val = self.conveyor_encoder.val
            print "Current encoder"
            print encoder_val
            print "Previous encoder value"
            print self.prev_encoder_value
            if abs(self.prev_encoder_value - encoder_val) <= 50:
                self.motor.write(False,250)
            self.prev_encoder_value = self.conveyor_encoder.val
            self.third_timer.reset()

        if self.second_timer.millis() > 300:
             self.second_timer.reset()
             if self.servo_val > self.CENTER:
                 self.servo.write(self.CENTER - 5)
                 self.servo_val = self.CENTER - 5
             else:
                 self.servo.write(self.CENTER + 5)
                 self.servo_val = self.CENTER + 5


             detect_red = self.color.r > 1.3*self.color.g
             detect_green = self.color.g > 1.3*self.color.r
             sum_val = self.color.r+self.color.g+self.color.b
             if detect_red and sum_val > 300:
                 self.servo.write(self.LEFT_TOWER)
                 self.servo_val = self.LEFT_TOWER
             elif detect_green and sum_val > 300:
                 self.servo.write(self.RIGHT_TOWER)
                 self.servo_val = self.RIGHT_TOWER
             else:
                 return

        if self.timer.millis() > self.INTERVAL:
            self.timer.reset()

            self.socket.send(b"need_image")
            message = self.socket.recv().split(",")

            # debug
            print message
            if message[0] == "None":				# no tower found
                lf = self.convertToInches(self.left_front.val)
                ls = self.convertToInches(self.left_side.val)
                rf = self.convertToInches(self.right_front.val)
                rs = self.convertToInches(self.right_side.val)

                print self.gyro.val

                if self.run_timer.millis() > self.RUN_TIME or lf < 11 or ls < 8.5 or rf < 9.3 or rs < 8.5:
                    print self.time_out.millis()
                    if self.run_timer.millis() < self.RUN_TIME:
                        if self.time_out.millis() > 10000:
                            self.motor_left.write(True, 30)
                            self.motor_right.write(False, 30)
                            return
                        print "COLLISION-DETECTED, adjusting"
                        if lf < 0:
                            lf = 100
                        if ls < 0:
                            ls = 100
                        if rf < 0:
                            rf = 100
                        if rs < 0:
                            rs = 100
                        detections = [ls < 8.5, lf < 11, rf < 9.3, rs < 8.5]
                        print detections
                        if detections == [True, True, True, True]:  # backup
							self.motor_left.write(False, 50)
							self.motor_right.write(False, 50)
                        elif detections == [True, True, True, False]:  # back up a bit and turn right
							self.motor_left.write(True, 50)
							self.motor_right.write(False, 50)	
                        elif detections == [False, True, True, True]: # back up a bit and turn left
							self.motor_left.write(False, 50)
							self.motor_right.write(True, 50)
                        elif detections == [True, True, False, False]:  # turn right
							self.motor_left.write(True, 50)
							self.motor_right.write(False, 50)
                        elif detections == [False, False, True, True]:  # turn left
							self.motor_left.write(False, 50)
							self.motor_right.write(True, 50)
                        elif detections == [True, False, False, False]: # turn slightly right
							self.motor_left.write(True, 45)
							self.motor_right.write(True, 20)
                        elif detections == [False, False, False, True]:  # turn slightly left
							self.motor_left.write(True, 20)
							self.motor_right.write(True, 45)
                        else:  # everything else, move up a bit
							self.motor_left.write(True, 30)
							self.motor_right.write(True, 30)
                        self.desired_angle = self.gyro.val
                        self.run_timer.reset()
                        return
                    else:
                        self.time_out.reset()
                        self.run_timer.reset()
                        self.desired_angle = random.randint(-90, 90) + self.gyro.val
                        self.RUNTIME = random.randint(3, 5) * 1000

                    print "DESIRED ANGLE:", self.desired_angle
                    diff = self.desired_center - self.gyro.val
                    power = self.PID_controller.power(diff)
                    self.motor_left.write(True, min(max(0, 50 + power), 50))
                    self.motor_right.write(True, min(max(0, 50 - power), 50))
            else:									# found a tower / blocks
                self.time_out.reset()
                diff = self.desired_center - int(message[1])
                if abs(diff) < 5 and int(message[2]) > 110:
                    self.STOP = True
                    return
                diff = 0 if abs(diff) < 2 else -diff
                power = self.PID_controller.power(diff)

                self.motor_left.write(True, min(max(0, 30 + power), 30))
                self.motor_right.write(True, min(max(0, 30 - power), 30))



    def convertToInches(self, value):
        inches = 0 if value <= 0 else -5.07243 * ln(0.0000185668 * value)
        return inches


if __name__ == "__main__":
    sketch = RandomBot(1, -0.00001, 100)
    sketch.run()
