#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from grove.button import Button
from grove.factory import Factory
from grove.gpio import GPIO
from libs import oled
from libs import led
from libs import music

# sphinx autoapi required
__all__ = ["LedButton", 'GroveLed', 'GPIO', 'Music']


class LedButton(object):

    def __init__(self, pin = 16):
        # High = light on
        self.buttonLed = Factory.getOneLed("GPIO-HIGH", pin)
        self.buttonLed.light(True)
        self.headLed = Factory.getOneLed("GPIO-HIGH", 8)
        self.headLed.light(True)
        self.led = Factory.getOneLed("GPIO-HIGH", 5)
        self.led.light(True)

        self.oled = oled.Oled()

        self.music = music.Music()

        # Low = pressed
        self.__btn = Factory.getButton("GPIO-LOW", pin + 1)
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
        self.led.brightness = self.led.MAX_BRIGHT
        self.headLed.brightness = self.headLed.MAX_BRIGHT

        event = evt['code']

        if event & Button.EV_DOUBLE_CLICK:
            self.buttonLed.light(True)
            self.led.light(True)
            self.headLed.light(True)

            print("EV_DOUBLE_CLICK")

        elif event & Button.EV_SINGLE_CLICK:
            self.buttonLed.blink()
            self.led.blink()
            self.headLed.blink()
            self.music.on()
            self.oled.show('Power On Gundam')

            print("EV_SINGLE_CLICK")

        elif event & Button.EV_LONG_PRESS:
            self.buttonLed.light(False)
            self.led.light(False)
            self.headLed.light(False)
            self.music.off()
            self.oled.show('Power Off Gundam')

            print("EV_LONG_PRESS")
        # elif event & Button.EV_LEVEL_CHANGED:
        #     print('EV LEVEL CHANGED')
            # self.oled.show('EV LEVEL CHANGED')


def main():
    pin = 16

    ledbtn = LedButton(pin)

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
