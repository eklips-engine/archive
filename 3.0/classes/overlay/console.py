import pygame as pg
import time, threading
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
		self.dt = 0.01
		self.text = "Sol Engine 0.20, Made by Za\n  type help for more info\n\n"
	
	def _show(self):
		while (self.y < 0):
			self.y += self.dt
	
	def _hide(self):
		while (self.y > -self.cs):
			self.y -= self.dt
		
	def _cmd(self, txt):
		self.text+=f"] {txt}\n"
		txtd=txt.split()
		self.cmd[len(self.cmd)] = txtd
	
	def show(self):
		t=threading.Thread(target=self._show)
		t.start()
		
	def hide(self):
		t=threading.Thread(target=self._hide)
		t.start()
	
	def draw(self, event=None):
		if self.y > -self.cs:
			frame = self.ux.frame((self.cw, self.cs), (0, self.y), id="ConsoleFr", alpha=.5)
			txt = self.res.render(self.text, color="black")
			self.ux.blit(txt, [20,20], disp=frame)
			self.ux.input((self.cw, 50), [0,0], anchor="bottom", id="ConsoleInp", placeholder="] Type something", disp=frame, frys=1, event=event)
			enter = self.ux.button(self.res.render("->", color="black"), [20,20], anchor="bottom right", disp=frame, frys=1)
			
			if self.ux.inputs["ConsoleInp"]["return"] or enter:
				if len(self.ux.inputs["ConsoleInp"]["value"].split()) > 0:
					frame["FrameObjData"]["y"] += 35
					self._cmd(self.ux.inputs["ConsoleInp"]["value"])
				else:
					frame["FrameObjData"]["y"] += 35
					self._cmd("var ExampleGame_ConsoleNotDoRun_IsTypeEquals 1")
				self.ux.inputs.pop("ConsoleInp")