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
			pass
		else:
			try:
				file = open(asset).read()
			except:
				file = None
			
			result = None
			try:
				ext = asset.split(".")[1]
			except:
				ext = "Extension[=ext]Unavailable"
			fnm = asset.split(".")[0]
			
			if ext == "json":
				try:
					result = json.loads(file)
				except:
					print("Broken asset")
			elif ext in ["png", "jpg", "jpeg"]:
				try:
					result = pg.image.load(asset)
				except:
					result = pg.Surface((200, 200))
					result.fill((255, 0, 0))
					print("Broken asset")
			elif ext == "sol":
				if file:
					result = file
				else:
					result = "broken=1"
			elif ext in ["wav", "mp3", "ogg"]:
				try:
					result = pg.mixer.Sound(asset)
				except:
					print("Broken asset")
			elif ext in ["zip", "pbd"]:
				try:
					result = zipfile.ZipFile(asset)
				except:
					print("Broken asset")
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
			pass
		else:
			result = pg.font.Font(font, size)
			
			self.resc[asset] = {
				"Font": font,
				"Size": size,
				"contents": result
			}
		
		return self.resc[asset]["contents"]
		
	def sheet(self, name):
		jsf=f"{self.resfol}/data/sheet/{name}.json"
		imf=f"{self.resfol}/media/sheet/{name}.png"
		#print(jsf,imf)
		return [self.load(jsf), self.load(imf)]
		
	def render(self, text, size=40, font="default", color=(255,255,255)):
		if font == "default":
			size = round(size * self.fnsmul)
		asset = f"RenderedFont-{size}{font}-{text}-{color}"
		if asset in self.resc:
			pass
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
		#print(f"Loading all files in '{fol}'")
		self.files = helper.list_files(fol)
		
		for asset in self.files:
			#print(f" |-> {asset}")
			self.load(asset)
		
		#print("Done Loading.")
		self.ldone = 1