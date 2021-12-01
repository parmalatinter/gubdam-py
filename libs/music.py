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

    def on(self):
        print("play music")
        self.mc.play_media('http://192.168.1.42/music-1.mp3', 'audio/mpeg', current_time=10, autoplay=True, title='gundam-1')
        self.mc.play()
        pychromecast.discovery.stop_discovery(self.browser)

    def off(self):
        print("stop music")
        self.mc.stop()
