
from driver.tamproxy import Sketch, SyncedSketch, Timer
from driver.tamproxy.devices import Encoder, Gyro, Motor


class StateMachine(SyncedSketch):

    
    def setup(self):
        
        self.states = {'SEARCH':0,'APPROACH':1,'INTAKE':2}
        self.transitions = {'found_something':False,'reached_location':False,'done_intaking':False}
        
        self.timer = Timer()

        self.current_state = self.states['SEARCH']
    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()

            if self.current_state == self.states['SEARCH']:
                print "do search stuff"
            elif self.current_state == self.states['APPROACH']:
                print "approach and stuff"
            else:
                print "intake everything"

            if self.current_state == self.states['SEARCH'] and self.transitions['found_something']:
                self.current_state = self.states['APPROACH']
                self.transitions['found_something'] = False
            elif self.current_state == self.states['APPROACH'] and self.transitions['reached_location']:
                self.current_state == self.states['INTAKE']
                self.transitions['reached_location'] = False
            elif self.current_state == self.states['INTAKE'] and self.transitions['done_intaking']:
                self.current_state = self.states['SEARCH']
                self.transitions['done_intaking'] = False


            

if __name__ == "__main__":
    sketch = StateMachine(1, -0.00001, 100)
    sketch.run()