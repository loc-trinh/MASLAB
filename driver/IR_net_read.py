from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import AnalogInput
from math import log as ln

# Detects changes in allllll the pins!

class SensorRead(SyncedSketch):

    left_front_pin = 10
    left_side_pin = 11
    right_front_pin = 12
    right_side_pin = 13

    prev_values_lf = [0] * 10
    prev_values_ls = [0] * 10
    prev_values_rf = [0] * 10
    prev_values_rs = [0] * 10
    counter = 0

    def setup(self):
        self.left_front = AnalogInput(self.tamp, self.left_front_pin)
        self.left_side = AnalogInput(self.tamp, self.left_side_pin)
        self.right_front = AnalogInput(self.tamp, self.right_front_pin)
        self.right_side = AnalogInput(self.tamp, self.right_side_pin)

                
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            self.prev_values_lf[self.counter % 10] = self.convertToInches(self.left_front.val)
            self.prev_values_ls[self.counter % 10] = self.convertToInches(self.left_side.val)
            self.prev_values_rf[self.counter % 10] = self.convertToInches(self.right_front.val)
            self.prev_values_rs[self.counter % 10] = self.convertToInches(self.right_side.val)
            
            
            if(self.counter >= 10):
                print "Left front: " + str(sum(self.prev_values_lf) / 10)
                print "Left side: " + str(sum(self.prev_values_ls) / 10)
                print "Right front: " + str(sum(self.prev_values_rf) / 10)
                print "Right side: " + str(sum(self.prev_values_rs) / 10)
            #print self.left
            self.counter += 1

    def convertToInches(self, value):
        '''LONG RANGE MODELS'''
        #first fitting function
        #print "first: " + str("{0:.2f}".format(-7.87402 * ln(value * .00001506809))) + " second: " + "{0:.2f}".format(-10.5363 * ln(0.0000188421 * value)) + " third: " +"{0:.2f}".format(-9.92063 * ln(0.0000171775 * value)) + " average: " +"{0:.2f}".format(-8.92307 * ln(0.0000166484 * value))
        #print "average of first and second: " + str("{0:.2f}".format(-10.3135 * ln(0.0000189117 * value)))
        #return -.127 * ln(value / 66362.0)
        #second fitting function
        #return -10.5363 * ln(0.0000188421 * value)
        #third fitting function
        #return -9.92063 * ln(0.0000171775 * value)
        #average of all models so far:
        #return -8.92307 * ln(0.0000166484 * value)
        #average of first and second:
        #return -10.3135 * ln(0.0000189117 * value)
        #^like this model the best
        #either that model or first one

        '''MID RANGE MODELS'''
        #first model:
        #return -5.47336 * ln(0.0000197638 * value)
        #second model:
        inches = 0 if value <= 0 else -5.07243 * ln(0.0000185668 * value)
        return inches
if __name__ == "__main__":
    sketch = SensorRead(1, -0.00001, 100)
    sketch.run()
