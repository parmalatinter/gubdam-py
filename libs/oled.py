#!/usr/bin/env python
# -*- coding: utf-8 -*-

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Change these
# to the right size for your display!
WIDTH = 128
#HEIGHT = 32  # Change to 64 if needed
HEIGHT = 64  # Change to 64 if needed
BORDER = 5

class Oled():
	def __init__(self):
		print(1)
		# Define the Reset Pin
		oled_reset = digitalio.DigitalInOut(board.D4)



		# Use for I2C.
		i2c = board.I2C()
		self.oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

		# Clear display.
		self.oled.fill(0)
		self.oled.show()
		self.postions = [(0,0), (0, 17), (0, 34), (0, 51)]

	def show(self, texts, selectIndex):
		# postions (0,0), (0, 17)
		# Clear display.
		self.oled.fill(0)
		self.oled.show()
		# Create blank image for drawing.
		# Make sure to create image with mode '1' for 1-bit color.
		image = Image.new("1", (self.oled.width, self.oled.height))

		# Get drawing object to draw on image.
		draw = ImageDraw.Draw(image)

		# Load default font.
		font = ImageFont.load_default()


		# Draw Some Text
		for index, text in enumerate(texts):
			if(index == selectIndex):
				text = '> ' + text

			draw.text(
				self.postions[index],
				text,
				font=font,
				fill=255
			)

		# Display image
		self.oled.image(image)
		self.oled.show()

	def off(self):

		self.oled.fill(0)
		self.oled.show()
