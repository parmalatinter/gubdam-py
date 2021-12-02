#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from grove.button import Button
from grove.factory import Factory
from grove.gpio import GPIO
from libs import oled
from libs import music
import threading

# sphinx autoapi required
__all__ = ['Led', "LedButton", 'GroveLed', 'GPIO', 'Music']

class Led(GPIO):

    def __init__(self, pin):
        super(Led, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)

    def blink(self):

        for i in range(100):
            self.on()
            time.sleep(0.5)
            self.off()
            time.sleep(0.5)


class LedThreading(threading.Thread):

    def __init__(self, thread_name, gpio):
        self.thread_name = str(thread_name)
        self.gpio = gpio
        threading.Thread.__init__(self)

    def __str__(self):
        return self.thread_name

    def run(self):
        self.gpio.blink()
        print('Thread: %s ended.' % self)

class LedButton(object):

    def __init__(self,):
        # High = light on
        self.buttonLed = Factory.getOneLed("GPIO-HIGH", 16)
        self.buttonLed.light(False)
        self.headLed = Led(8)
        self.headLed.off()
        self.led = Led(5)
        self.led.off()
        self.bodyLed = Led(22)
        self.bodyLed.off()

        self.oled = oled.Oled()

        self.music = music.Music()
        self.music.off()

        # Low = pressed
        self.__btn = Factory.getButton("GPIO-LOW", 16 + 1)
        self.__on_event = None
        self.__btn.on_event(self, LedButton.__handle_event)

        self.oled.show('This is The Gundam')

    @property
    def on_event(self):
        return self.__on_event

    @on_event.setter
    def on_event(self, callback):
        if not callable(callback):
            return
        self.__on_event = callback

    def __handle_event(self, evt):
        print("event index:{} event:{}".format(evt['index'], evt['code']))

        if callable(self.__on_event):
            # the customized behavior
            self.__on_event(evt['index'], evt['code'], evt['time'])
            return

        self.buttonLed.brightness = self.buttonLed.MAX_BRIGHT
        # self.led.brightness = self.led.MAX_BRIGHT
        # self.headLed.brightness = self.headLed.MAX_BRIGHT

        event = evt['code']

        if event & Button.EV_DOUBLE_CLICK:
            self.buttonLed.light(True)
            self.led.off()
            self.headLed.off()
            self.bodyLed.off()

            print("EV_DOUBLE_CLICK")

        elif event & Button.EV_SINGLE_CLICK:
            self.music.on()

            thread1 = LedThreading(thread_name=1, gpio=self.led).start()
            thread2 = LedThreading(thread_name=2, gpio=self.headLed).start()
            thread3 = LedThreading(thread_name=3, gpio=self.bodyLed).start()
            thread_list.append(thread1)
            thread_list.append(thread2)
            thread_list.append(thread3)

            self.oled.show('Power On Gundam')

            print("EV_SINGLE_CLICK")

        elif event & Button.EV_LONG_PRESS:
            self.buttonLed.light(False)
            self.led.off()
            self.headLed.off()
            self.bodyLed.off()
            self.music.off()
            self.oled.show('Power Off Gundam')

            print("EV_LONG_PRESS")
        # elif event & Button.EV_LEVEL_CHANGED:
        #     print('EV LEVEL CHANGED')
            # self.oled.show('EV LEVEL CHANGED')


def main():
    ledbtn = LedButton()

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
