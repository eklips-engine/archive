import pygame as pg
from classes import ui

class Overlay:
	def __init__(self, ux):
		self.ux = ux
		self.overlay = {}
	
	def update(self, **args):
		return self.ux.blit(args)