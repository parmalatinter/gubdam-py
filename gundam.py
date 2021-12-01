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
        self.led = Factory.getOneLed("GPIO-HIGH", pin)
        self.led.light(True)
        self.led2 = led.Led(5)
        self.music = music.Music()
        # Low = pressed
        self.__btn = Factory.getButton("GPIO-LOW", pin + 1)
        self.__on_event = None
        self.__btn.on_event(self, LedButton.__handle_event)
        self.oled = oled.Oled()
        self.headLed = led.Led(8)
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
        # print("event index:{} event:{} pressed:{}"
        #       .format(evt['index'], evt['code'], evt['presesed']))
        if callable(self.__on_event):
            # the customized behavior
            self.__on_event(evt['index'], evt['code'], evt['time'])
            return

        # the default behavior
        self.led.brightness = self.led.MAX_BRIGHT

        event = evt['code']
        if event & Button.EV_SINGLE_CLICK:
            self.led.light(True)
            self.led2.on()
            self.music.on()
            self.oled.show('Power On Gundam')
            self.headLed.blight()

        elif event & Button.EV_DOUBLE_CLICK:
            self.led.blink()
            print("blink    LED")
        elif event & Button.EV_LONG_PRESS:
            self.led.light(False)
            self.led2.off()
            self.music.off()
            self.oled.show('Power Off Gundam')
            self.headLed.off()
        elif event & Button.EV_LEVEL_CHANGED:
            self.oled.show('EV LEVEL CHANGED')


def main():
    pin = 16

    ledbtn = LedButton(pin)

    # remove ''' pairs below to begin your experiment
    '''
    # define a customized event handle your self
    def cust_on_event(index, event, tm):
        print("event with code {}, time {}".format(event, tm))

    ledbtn.on_event = cust_on_event
    '''
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
