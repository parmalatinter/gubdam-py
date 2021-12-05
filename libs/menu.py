#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Menu():

	def __init__(self, oled):
		self.oled = oled
		self.checked = '✓'

		self.unChecked = ' '

		self.selectIndex = 0
		self.menus = [ 'Menu1', 'Menu2', 'Menu3', 'Menu4']
		self.oled.show(self.menus, self.selectIndex)

	def clear(self):
		self.oled.off()


	def select(self):
		self.selectIndex += 1
		if(self.selectIndex > len(self.menus)-1):
			self.selectIndex = 0

		self.oled.show(self.menus, self.selectIndex)

	def getIndex(self):
		return self.selectIndex
