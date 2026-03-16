import pygame as pg
from pygame.locals import *

# Define gravitational constants
gravity_factor = .5
gravity = 9.8 * gravity_factor

class PhysicsBody:
	def __init__(self, rect, color="white", bf=.1, wgt=1, vel=[0,0]):
		self.rect                    = rect
		self.bouncy              = 1
		self.vel_x                  = vel[0]
		self.vel_y                  = vel[1]
		self.weight               = wgt
		self.friction              = 0.1
		self.touched            = 0
		self.rel                       = [0,0]
		self.bounce_count   = 0
		self.bounce_factor  = bf
		self.col                      = color
	
	def _updvel(self, dt):
		self.vel_y += (gravity * self.weight * (dt * 20)) / 10
		if self.vel_x > 0:
			self.vel_x -= self.friction * dt
			if self.vel_x < 0:
				self.vel_x = 0
		elif self.vel_x < 0:
			self.vel_x += self.friction * dt
			if self.vel_x > 0:
				self.vel_x = 0
	
	def _updevent(self, event):
		if pg.mouse.get_pressed()[0]:
			pos = pg.mouse.get_pos()
			colliding=self.rect.collidepoint(pos)
			if colliding:
				self.touched = 1
		else:
			if self.touched:
				self.vel_x = self.rel[0] / (self.weight+.5)
				self.vel_y = self.rel[1] / (self.weight+.5)
				self.touched = 0
	
	def _updmove(self):
		self.rect.x += self.vel_x
		self.rect.y += self.vel_y
		if self.touched:
			self.rel = list(pg.mouse.get_rel())
			mpos   = pg.mouse.get_pos()
			self.rect.move_ip(self.rel[0] / (self.weight+.5), self.rel[1] / (self.weight+.5))
			self.vel_x = 0
			self.vel_y = 0
			self.bouncy = 1
			self.bounce_count = 0
	
	def _getevent(self):
		return pg.event.get()
	
	def update(self, surface, dt):
		self._updvel(dt)
		self._updbnc(dt)
		self._updevent(self._getevent())
		self._updmove()
		self._draw(surface)
	
	def _updbnc(self, dt):
		if self.rect.y < 1:
			self.rect.y = 0
			self.vel_y = abs(self.vel_y) / self.bouncy
			self.bounce_count += 1
		elif self.rect.y > surface.get_height() - self.rect.h:
			self.rect.y = surface.get_height() - self.rect.h
			self.vel_y = -self.vel_y / self.bouncy
			if abs(self.vel_y) > 0.4:
				self.bounce_count += 1
		elif self.rect.x < 1:
			self.rect.x = 0
			self.vel_x = -self.vel_x / self.bouncy
			self.bounce_count += 1
		elif self.rect.x > surface.get_width() - self.rect.w:
			self.rect.x = surface.get_width() - self.rect.w
			self.vel_x = -self.vel_x / self.bouncy
			self.bounce_count += 1
		else:
			self.bouncy += self.bounce_factor * dt
		
	def _draw(self, surface):
		pg.draw.rect(surface, self.col, self.rect)