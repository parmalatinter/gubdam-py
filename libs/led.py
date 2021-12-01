import time
from grove.gpio import GPIO

__all__ = ['Led', 'GPIO']

class Led(GPIO):

    isOn = False


    def __init__(self, pin):
        super(Led, self).__init__(pin, GPIO.OUT)

    def on(self):

        self.write(1)

    def off(self):

        self.write(0)
        self.isOn = False

    def blight(self):
        self.isOn = True

        while self.isOn:
            self.on()
            time.sleep(1)
            self.off()
            time.sleep(1)


