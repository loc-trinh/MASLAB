from driver.tamproxy import Sketch, Timer

class Camera(Sketch):
    def setup(self):
        self.led_timer = Timer()
        self.counter = 0

    def loop(self):
        if self.led_timer.millis() > 100:
            self.led_timer.reset()

if __name__ == "__main__":
    sketch = Camera()
    sketch.run()