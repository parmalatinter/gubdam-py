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

	def show(self, text):

		# Clear display.
		self.oled.fill(0)
		self.oled.show()
		# Create blank image for drawing.
		# Make sure to create image with mode '1' for 1-bit color.
		image = Image.new("1", (self.oled.width, self.oled.height))

		# Get drawing object to draw on image.
		draw = ImageDraw.Draw(image)

		# Draw a white background
		draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)

		# Draw a smaller inner rectangle
		draw.rectangle(
		    (BORDER, BORDER, self.oled.width - BORDER - 1, self.oled.height - BORDER - 1),
		    outline=0,
		    fill=0,
		)

		# Load default font.
		font = ImageFont.load_default()

		# Draw Some Text
		(font_width, font_height) = font.getsize(text)
		draw.text(
		    (self.oled.width // 2 - font_width // 2, self.oled.height // 2 - font_height // 2),
		    text,
		    font=font,
		    fill=255,
		)

		# Display image
		self.oled.image(image)
		self.oled.show()

	def off(self):

		self.oled.fill(0)
		self.oled.show()
