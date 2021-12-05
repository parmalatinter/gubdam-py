#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
from grove.button import Button
from grove.factory import Factory
from grove.gpio import GPIO
from libs import oled
from libs import music
from libs import led
from libs import const
from libs import button

# sphinx autoapi required
__all__ = ['LedButton', 'GPIO', 'NormalButton']


const.FOO = 100
const.BAR = 'Hello'

class LedButton(object):

    def __init__(self):
        print(const.FOO)
        # High = light on
        self.button = button.NormalButton(24)
        self.button.on_press = self.on_press
        self.button.on_release = self.on_release

        self.buttonLed = Factory.getOneLed("GPIO-HIGH", 16)
        self.buttonLed.light(False)
        self.headLed = led.Led(8)
        self.headLed.off()
        self.led = led.Led(5)
        self.led.off()
        self.bodyLed = led.Led(22)
        self.bodyLed.off()

        self.oled = oled.Oled()

        self.music = music.Music()
        self.music.off()

        # Low = pressed
        self.__btn = Factory.getButton("GPIO-LOW", 16 + 1)
        self.__on_event = None
        self.__btn.on_event(self, LedButton.__handle_event)

        self.oled.show('This is The Gundam')

    def on_press(self, t):
        self.music.on('http://192.168.1.42/rifle.wav', 'audio/wav')
        self.bodyLed.on()
        time.sleep(1)
        self.bodyLed.off()
        print('Button is pressed')

    def on_release(self, t):
        print("Button is released, pressed for {0} seconds".format(round(t,6)))

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
        event = evt['code']

        if event & Button.EV_DOUBLE_CLICK:
            self.buttonLed.light(True)
            self.led.off()
            self.headLed.off()
            self.bodyLed.off()

            print("EV_DOUBLE_CLICK")

        elif event & Button.EV_SINGLE_CLICK:
            self.music.on('http://192.168.1.42/music-1.mp3', 'audio/mp3')

            thread_list = threading.enumerate()
            thread1 = led.LedThreading(thread_name=1, led=self.led, option={'method' : 'blink', 'count': 100}).start()
            thread2 = led.LedThreading(thread_name=2, led=self.headLed, option={'method' : 'blink', 'count': 100}).start()
            thread3 = led.LedThreading(thread_name=3, led=self.bodyLed, option={'method' : 'blink', 'count': 100}).start()
            thread_list.append(thread1)
            thread_list.append(thread2)
            thread_list.append(thread3)

            self.oled.show(['Power On Gundam'], [[0,0]])


            print("EV_SINGLE_CLICK")

        elif event & Button.EV_LONG_PRESS:
            self.buttonLed.light(False)
            self.led.off()
            self.headLed.off()
            self.bodyLed.off()
            self.music.off()
            self.oled.show(['Power Off Gundam'], [[0,0]])

            print("EV_LONG_PRESS")


def main():
    ledbtn = LedButton()

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
