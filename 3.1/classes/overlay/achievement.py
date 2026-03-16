import pygame as pg
import time
from classes import ui
from classes.overlay import console, achievement, _overlay

ach = []
print(__file__)

class Achievement(_overlay.Overlay):
	def __init__(self, ux, fs):
		_overlay.Overlay.__init__(self, ux)
		self.fs = fs
		self.ux = ux
	
	def add(self, name):
		self.fs.set(f"Account/offline_achievements/{name}", [1, time.strftime("%B %d, %Y at %I:%M:%S %p")])
		self.apiblit(name)
	
	def rem(self, name):
		self.fs.set(f"Account/offline_achievements/{name}", [0,0])
	
	def apiblit(self, name):
		ach.append(name)