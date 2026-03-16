import pygame as pg
import time, threading, os
from classes import ui
from classes.overlay import console, achievement, _overlay

class Console(_overlay.Overlay):
	def __init__(self, ux, res):
		_overlay.Overlay.__init__(self, ux)
		self.ux = ux
		self.res = res
		self.cs = int(round(self.ux.display.get_height() / 2))
		self.cw = self.ux.display.get_width()
		self.y = -self.cs
		self.cmd = {}
		self.dt = 0.00001
		self.d=0
		self.bgr=0
		self.text = "Eklips Engine Console\nType 'help' to get a list of commands\n\n"
		self.cooldownsh = 0
	
	def show(self):
		self.y = 0
	
	def hide(self):
		self.y = -self.cs
		
	def _cmd(self, txt):
		txt=str(txt).replace("`","")
		self.printf(f"] {txt}")
		txtd=txt.split()
		if txt == "help":
			expr_out = (i.lstrip('.sol') for i in os.listdir(open('game.txt').read().splitlines()[1]+'/data/scripts/cmd'))
			self.printf(str(expr_out))
		elif txt == "emer":
			self.y = -self.cs
		else:
			self.cmd[len(self.cmd)] = txtd
	
	def printf(self, text):
		self.text += str(text) + "\n"
		self.d = len(text.splitlines())
	
	def blit(self, event=None):
		if self.y > -self.cs:
			self.ux.blit(self.ux.rect("white", (self.cw, self.cs+100)),[0,10],layer=234)
			self.ux.blit(self.ux.rect("black", (self.cw, self.cs+100)),[0,0],layer=235)
			oldtext=self.text.split("\n")
			if len(oldtext)+3 > (self.cs/27):
				for i in range(round(len(oldtext)+3 - self.cs/27)):
					oldtext.pop(0)
			self.text="\n".join(oldtext)
				
			txt = self.res.render(self.text, color="white",cache=0)
			txts = self.res.render("e",cache=0)
			self.ux.blit(txt, [20,60], layer=237, add_bg=0)
			self.ux.input((50, 50), [0,0], anchor="", id="ConsoleInp", event=event, color="white", AlwaysOn=1,layer=236)
			
			if self.ux.inputs["ConsoleInp"]["return"]:
				if len(self.ux.inputs["ConsoleInp"]["value"].split()) > 0:
					self._cmd(self.ux.inputs["ConsoleInp"]["value"])
				self.ux.inputs.pop("ConsoleInp")