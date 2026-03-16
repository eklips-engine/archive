## Import
import pygame as pg
import json, os, zipfile, time
from classes import helper

## Init
pg.init()

## class
class ResourceLoader:
	def __init__(self, resfol="resources"):
		self.resfol = resfol
		self.resc = {}
		self.ldone = 0
		self.files = {}
		self.deffnt = None
		self.fnsmul = 1
	
	def modfont(self, name):
		self.deffnt = name
		self.fnsmul = .75
	
	def load(self, asset):
		if asset in self.resc or os.path.isdir(asset):
			print(end="")
		else:
			try:
				file = open(asset).read()
			except:
				file = None
			
			result = None
			ext = asset.split(".")[1]
			fnm = asset.split(".")[0]
			
			if ext == "json":
				result = json.loads(file)
			elif ext in ["png", "jpg", "jpeg"]:
				result = pg.image.load(asset)
			elif ext in ["wav", "mp3", "ogg"]:
				result = pg.mixer.Sound(asset)
			elif ext in ["zip", "pbd"]:
				result = zipfile.ZipFile(asset)
			else:
				result = file
			
			self.resc[asset] = {
				"ext": ext,
				"fnm": fnm,
				"contents": result
			}
		
		return self.resc[asset]["contents"]
	
	def get_font(self, font, size):
		asset = f"Font-{font}-{size}"
		if asset in self.resc:
			print(end="")
		else:
			result = pg.font.Font(font, size)
			
			self.resc[asset] = {
				"Font": font,
				"Size": size,
				"contents": result
			}
		
		return self.resc[asset]["contents"]
			
	def render(self, text, size=40, font="default", color=(255,255,255)):
		if font == "default":
			size = round(size * self.fnsmul)
		asset = f"RenderedFont-{size}{font}-{text}-{color}"
		if asset in self.resc:
			print(end="")
		else:
			if font == "default":
				font = self.deffnt
			hdtxt = pg.Surface((1080,1080), pg.SRCALPHA)
			
			y = 0
			x = 0
			font = self.get_font(font, size)
			text = str(text).split("\n")
			render = 0
			
			for i in text:
				render = font.render(i, 0, color)
				hdtxt.blit(render, [0,y])
				y += render.get_height()
				if render.get_width() > x:
					x = render.get_width()
			
			result = pg.Surface((x, y), pg.SRCALPHA)
			result.blit(hdtxt, [0,0])
			
			self.resc[asset] = {
				"Font": font,
				"Size": size,
				"Text": text,
				
				"contents": result
			}
		
		return self.resc[asset]["contents"]
	def load_all(self, fol="defaultGame"):
		self.ldone = 0
		if fol == "defaultGame":
			fol=self.resfol
		print(f"Loading all files in '{fol}'")
		self.files = helper.list_files(fol)
		
		for asset in self.files:
			print(f" |-> {asset}")
			self.load(asset)
		
		print("Done Loading.")
		self.ldone = 1