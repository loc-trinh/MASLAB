from driver.tamproxy import SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro, Motor, AnalogInput, Color, Servo
import random
import zmq
from math import log as ln


class PID:
    def __init__(self, dT):
        self.Kp = 3
        self.Ki = .5
        self.Kd = -.5
        self.last_diff = 0
        self.integral = 0
        self.dT = dT

    def power(self, diff):
        self.integral += diff * self.dT
        derivative = float(self.last_diff - diff) / self.dT
        power = self.Kp * diff + self.Ki * self.integral + self.Kd * derivative
        self.last_diff = diff
        return power


class MainBot(SyncedSketch):
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
        self.servo.write(self.CENTER+10)
        self.servo_val = self.CENTER-10

        self.servo_bottom = Servo(self.tamp,22)
        self.servo_bottom.write(34)
        self.sorter_timer = Timer()

        # ============== Intake setup ============ #
        self.motor = Motor(self.tamp, 24, 25)
        self.motor.write(True, 0)

        self.conveyor_encoder = Encoder(self.tamp, 32,32, continuous=True)
        self.conveyor_encoder.update()

        self.prev_encoder_value = 0
        self.intake_timer = Timer()

        # ============== State Machine setup =========== #
        self.state = "SEARCH"
        self.state_timer = Timer()
        #for search
        self.turn_timer = Timer()
        self.sign = 1

    def loop(self):
        if self.sorter_timer.millis() > 300:
            self.sorter_timer.reset()
            if self.servo_val > self.CENTER:
                self.servo.write(self.CENTER - 8)
                self.servo_val = self.CENTER - 8
            else:
                self.servo.write(self.CENTER + 8)
                self.servo_val = self.CENTER + 8

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

        if self.intake_timer.millis() > 100:
            self.motor.write(True,125)
            encoder_val = self.conveyor_encoder.val
            if abs(self.prev_encoder_value - encoder_val) <= 50:
                self.motor.write(False,150)
            self.prev_encoder_value = encoder_val
            self.intake_timer.reset()

        if self.timer.millis() > 30:
            self.timer.reset()

            if self.state == "SEARCH":
                self.socket.send(b"get_image")
                message = self.socket.recv()
                message = message.split(",")
                if message[0] == "None":
                    if self.turn_timer.millis() > 3000:
                        self.turn_timer.reset()
                        self.sign *= -1
                    diff = 90 * self.sign
                else:
                    diff = int(message[1]) - 80
                    if abs(diff) < 3:
                        diff = 0

                power = self.PID_controller.power(diff)
                speed = min(30, abs(power))

                if abs(speed) < 10:
                    speed = 0

                if power >= 0:
                    self.motor_left.write(True, speed)
                    self.motor_right.write(False, speed)
                else:
                    self.motor_left.write(False, speed)
                    self.motor_right.write(True, speed)

                if self.state_timer.millis() > 9000:
                    if message[0] != "None":
                        self.motor_left.write(True, 0)
                        self.motor_right.write(True, 0)
                        self.state_timer.reset()
                        self.state = "APPROACH"
                    else:
                        self.motor_left.write(True, 0)
                        self.motor_right.write(True, 0)
                        self.state_timer.reset()
                        self.state = "EXPLORE"

            if self.state == "APPROACH":
                self.socket.send(b"get_image")
                message = self.socket.recv()
                message = message.split(",")
                #Message None is not an option

                diff = int(message[1]) - self.desired_center

                if abs(diff) < 5 and int(message[2]) > 108:
                    self.motor_left.write(True, 0)
                    self.motor_right.write(True, 0)
                    self.state_timer.reset()
                    self.state = "COLLECT"

                diff = 0 if abs(diff) < 5 else diff
                power = self.PID_controller.power(diff)

                self.motor_left.write(True, min(max(0, 30 + power), 30))
                self.motor_right.write(True, min(max(0, 30 - power), 30))

                if self.state_timer.millis() > 8000:
                    self.motor_left.write(True, 0)
                    self.motor_right.write(True, 0)
                    self.state_timer.reset()
                    self.state = "EXPLORE"


            if self.state == "COLLECT":
                self.motor_left.write(True, 50)
                self.motor_right.write(True, 50)
                if self.state_timer.millis() > 2000:
                    self.motor_left.write(True, 0)
                    self.motor_right.write(True, 0)
                    self.state_timer.reset()
                    self.state = "STOP"

            


    def convertToInches(self, value):
        inches = 0 if value <= 0 else -5.07243 * ln(0.0000185668 * value)
        return inches


if __name__ == "__main__":
    sketch = MainBot(1, -0.00001, 100)
    sketch.run()
