#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pychromecast

class Music():

    def __init__(self):
        # Discover and connect to chromecasts named Living Room
        self.chromecasts, self.browser = pychromecast.get_listed_chromecasts(friendly_names=["ダイニングルーム"])
        cast = self.chromecasts[0]
        cast.wait()
        self.mc = cast.media_controller
        print(self.mc.status)

    def on(self, path, type):
        print("play music")
        self.mc.play_media(path, type)
        self.mc.play()
        pychromecast.discovery.stop_discovery(self.browser)

    def off(self):
        print("stop music")
        self.mc.stop()
