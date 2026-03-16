import pygame as pg

pg.init()
class SoundSystem:
	def __init__(self):
		self.sfx = {}
	
	def play(self, sfx, pos_to=[0,0], pos_at=[0,0],loop=0):
		id = f"Sound-{len(self.sfx)}"
		sfx.play()
		self.sfx[id] = [sfx, pos_to, loop]
	
	def sound_done(self):
		self.sfx={}