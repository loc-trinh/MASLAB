from driver.tamproxy import SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro, Motor, AnalogInput
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

        # ============ Sorting & conveyor setup ============ #
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
        self.second_timer = Timer()

    def loop(self):
        if self.second_timer.millis() > 300:
            self.second_timer.reset()
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

                # print lf, ls, rf, rs

                if self.run_timer.millis() > self.RUN_TIME or lf < 9 or ls < 7 or rf < 9 or rs < 7:
                    if self.run_timer.millis() < self.RUN_TIME:
                        print "COLLISION-DETECTED, adjusting"
                        detections = [lf < 9, ls < 7, rf < 9, rs < 7]
                        print detections
                        if detections == [True, True, True, True]:  # backup
							self.motor_left.write(False, 50)
							self.motor_right.write(False, 50)
							return
                        elif detections == [True, True, True, False]:  # back up a bit and turn right
							self.motor_left.write(True, 50)
							self.motor_right.write(False, 50)
							return		
                        elif detections == [False, True, True, True]: # back up a bit and turn left
							self.motor_left.write(False, 50)
							self.motor_right.write(True, 50)
							return	
                        elif detections == [True, True, False, False]:  # turn right
							self.motor_left.write(True, 20)
							self.motor_right.write(True, 40)
							return	
                        elif detections == [False, False, True, True]:  # turn left
							self.motor_left.write(True, 40)
							self.motor_right.write(True, 20)
							return
                        elif detections == [True, False, False, False] or detections == [False, True, False, True]: # turn slightly right
							self.motor_left.write(True, 20)
							self.motor_right.write(True, 30)
							return
                        elif detections == [False, False, False, True] or detections == [False, False, True, False]:  # turn slightly left
							self.motor_left.write(True, 30)
							self.motor_right.write(True, 20)
							return
                        else:  # everything else, move up a bit
							self.motor_left.write(False, 30)
							self.motor_right.write(False, 30)
							return
                    else:
                        self.run_timer.reset()
                        self.desired_angle = random.randint(-60, 60)
                        self.RUNTIME = random.randint(3, 5) * 1000

                    print "DESIRED ANGLE:", self.desired_angle
                    diff = self.desired_center - self.gyro.val
                    power = self.PID_controller.power(diff)
                    self.motor_left.write(True, min(max(0, 50 + power), 50))
                    self.motor_right.write(True, min(max(0, 50 - power), 50))
            else:									# found a tower / blocks
                diff = self.desired_center - int(message[1])
                diff = 0 if abs(diff) < 2 else -diff
                power = self.PID_controller.power(diff)

                self.motor_left.write(True, min(max(0, 50 + power), 50))
                self.motor_right.write(True, min(max(0, 50 - power), 50))



    def convertToInches(self, value):
        inches = 0 if value <= 0 else -5.07243 * ln(0.0000185668 * value)
        return inches


if __name__ == "__main__":
    sketch = RandomBot(1, -0.00001, 100)
    sketch.run()
