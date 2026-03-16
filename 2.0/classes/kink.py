# Kink Video Reader
import zipfile, json, os, shutil
import pygame as pg

## Init
pg.init()

## Classes
class KinkVid:
	def __init__(self, ux, resld):
		self.videos = {}
		self.ux = ux
		self.resld = resld
	
	def update(self, dt=1):
		remvid = None
		
		for i in self.videos:
			if round(self.videos[i]["Frame"]+dt) in self.videos[i]["Frames"]:
				self.videos[i]["Frame"] += dt
				
				frameid =  round(self.videos[i]["Frame"])
				frame = self.videos[i]["Frames"][frameid]
				
				pos = self.videos[i]["Pos"]
				
				self.ux.blit(frame, pos, scale=3)
			else:
				remvid = i
				print(f"VidDone{i}")
		
		if remvid:
			self.videos.pop(i)
	
	def load(self, kfile, pos=[0,0]):
		kfileid = kfile.split("/")[-1].split(".")[0] #KinkFileID
		kdir = f"kink/Archive{kfileid}" #KinkDir
		zip = zipfile.ZipFile(kfile)
		zip.extractall(kdir)
		
		meta = json.loads(open(f"{kdir}/meta.json").read())
		
		print(f"Loading Video {kfile}")
		frames = {} # Frames
		frame = meta["StartFrame"] # Cycle Frame
		sframe = frame # Starting Frame
		for i in os.listdir(f"{kdir}/vid"):
			loadframe = self.resld.load(f"{kdir}/vid/{i}")
			frames[frame] = loadframe
			frame += 1
		
		self.videos[kfileid] = {
			"Frame": sframe,
			"ZipObj": zip,
			"Meta": meta,
			
			"Frames": frames,
			
			"Pos": pos
		}
		print("Done")
		shutil.rmtree(kdir)