## Import
import pygame as pg
import tkinter
import traceback, socket, threading
import ekhl, moderngl as mgl
import time
import gc, psutil
import classes.overlay as overlay
from tkinter import ttk
from tkinter.messagebox import *
import os, time, json, threading, random, requests
from classes import ekeng, res, fs, ui, sfxsys, kink, network as net, markov
from classes.overlay import console, achievement, _overlay
import copy

## Init
pg.init()
GCT = 0

## Display
display_size = pg.display.list_modes()[0]
flags = pg.FULLSCREEN
display=0
def setdisp(isSplash=0,resolution="full"):
	global display, display_size, flags
	if isSplash:
		if resolution=="":
			display = pg.display.set_mode((450,300), pg.NOFRAME)
		else:
			try:
				display = pg.display.set_mode(resolution.get_size(), pg.NOFRAME)
			except:
				display = pg.display.set_mode((450,300), pg.NOFRAME)
	else:
		if resolution=="full":
			display = pg.display.set_mode(display_size, flags)
		else:
			display = pg.display.set_mode(resolution, 0)

resfol=open("game.txt").read().splitlines()[1]

## Caption
pg.display.set_caption(open("game.txt").read().splitlines()[0])

## Clock
clock = pg.time.Clock()

## Filesystem
fsm = fs.Filesystem(open("game.txt").read().splitlines())
ctx=0
if fsm.get("Settings/performance/UseGPU", 0):
	gpumode=1
	flags = pg.OPENGL | pg.DOUBLEBUF
	print("Using GPU")
	display = pg.display.set_mode(display_size, flags)
	ctx = mgl.create_context()
else:
	gpumode=0
	setdisp(resolution=fsm.get("Settings/display/res","full"))

## RescLoader
resld = res.ResourceLoader(resfol)

## Icon
try:
	pg.display.set_icon(resld.load(f"{resld.resfol}/media/icon.png"))
except:
	pg.display.set_icon(resld.load(f"{resld.resfol}/media/eklips/icon.png"))

## Poem
poem = markov.Poem()

## SoundSystem
sfx = sfxsys.SoundSystem()
sfx.dvol = fsm.get("Settings/volume/mastervolume")

## User Interface
#display, sfx, clk, res, gpumode, ctx
ux = ui.Interface(display, sfx, resld.load(f"{resld.resfol}/media/click.mp3"), resld, gpumode, ctx)

## KinkReader
kinkr = kink.KinkVid(ux, resld)

## Eklips related
try:
	sol_ver = open(f"{resld.resfol}/ver.txt").read().splitlines()[1]
except:
	sol_ver = "unknown"
ekl = ekeng.Engine()
solengi = ekl
solcons = console.Console(ux, resld)
solwid = f"{resld.resfol}/{resld.resfol}.wid"

## Variables
running = 1
ticks = 1
fticks = 0
latest_key = 0

## Delta Time
old_dt = time.time()
dt = time.time()

## Game Data
data = {
	"Engine": {
		"MainMenu": 1,
		"Scene": "main",
		
		"Transition": "",
		"TAlpha": 0,
		"TAF": 1,
		"TSpeed": 1,

		"bsod": {
			"stage": 0
		},
		
		"GameAnimSpeed": 1,
		"Player": {
			"Pos": [0,0],
			"Vel": [10,10],
			"Flp": 0,
			"SessionName": 0,
			"Inventory": []
		},
		"CVar": {},
		"Level": {
			"Objects": {}
		}
	},
	
	"Lang": {},
	"LU": "",
	"Debug": 1
}

def servref(ip="", debug=0):
	e=net.ServerList(ip)
	return e.out

servers={}

## Loader
loadscr = 1
loadthread = None
loading = 0
ldt = 0
ldts = 1
loadskp = fsm.get("Settings/load/loadskip")
loadno = fsm.get("Settings/load/noload")

## InstancePlayer properties
try:
	playermod = ekl.read(f"{resld.resfol}/data/instances/player.sol")["info"]
except:
	playermod = ekl.read(f".ekeng/player.sol")["info"]
	print("Eklips playermod gone, game errors expected")

## Spritesheet
try:
	playersheet = resld.sheet(playermod["file"])
except:
	print("Eklips playersheet gone, game errors expected")

## Menu assets
bg = resld.load(resld.resfol+"/media/bg.png")
bg = pg.transform.scale(bg, display.get_size())
bgr=1
oldprlx=0
prlxs={}
for i in range(len(os.listdir(resld.resfol+"/media/prlx"))):
	prlx=resld.load(f"{resld.resfol}/media/prlx/prlx{i}.png")
	prlx = pg.transform.scale(prlx, (prlx.get_width()/2, prlx.get_height()/2))
	prlxs[i+1]=prlx
bge=pg.Surface([bg.get_width(),prlxs[1].get_height()])
bge.blit(bg, [0,0], [0,bg.get_height()-prlxs[1].get_height(),bg.get_width(),prlxs[1].get_height()])
prlxw=prlxs[1].get_width()
logotxt = resld.render(fsm.gm[0])

try:
	ev="start"
	ekl.run(f"{resld.resfol}/data/scripts/event/{ev}.sol", gl=globals(), lc=locals())
except:
	print("Event error")

speed=1

resld.deffnt = fsm.get("Settings/private/Font").replace("\\","/").replace("]",resfol+"/")
if not resld.deffnt:
	resld.deffnt = None
resld.fnsmul = fsm.get("Settings/private/Size")
rendalpha = fsm.get("Settings/private/SupportsAlpha")

def _load_all_eng():
	global running,ux,sfx,ticks,fticks,latest_key,playermod,playersheet,bg,bgr,load_done,oldprlx,prlxs,prlxw,logotxt,rendalpha,resld
	print("Setting up icon")
	try:
		pg.display.set_icon(resld.load(f"{resld.resfol}/media/icon.png"))
	except:
		pg.display.set_icon(resld.load(f"{resld.resfol}/media/eklips/icon.png"))
	print("Setting up libraries")
	print(" - poem")
	poem = markov.Poem()
	print(" - sfx")
	sfx = sfxsys.SoundSystem()
	sfx.dvol = fsm.get("Settings/volume/mastervolume")
	print(" - ux")
	ux = ui.Interface(display, sfx, resld.load(f"{resld.resfol}/media/click.mp3"), resld, gpumode, ctx)
	print("Setting up values")
	print(" - runnable")
	running = 1
	ticks = 1
	fticks = 0
	latest_key = 0
	print(" - playermod")
	try:
		playermod = ekl.read(f"{resld.resfol}/data/instances/player.sol")["info"]
	except:
		playermod = ekl.read(f".ekeng/player.sol")["info"]
		print("Eklips playermod gone, game errors expected")

	print(" - player spritesheet")
	try:
		playersheet = resld.sheet(playermod["file"])
	except:
		print("Eklips playersheet gone, game errors expected")

	## Menu assets
	print("Loading menu assets\n - bg")
	bg = resld.load(resld.resfol+"/media/bg.png")
	bg = pg.transform.scale(bg, display.get_size())
	print(" - bgr")
	bgr=1
	oldprlx=0
	prlxs={}
	print(" - prlx")
	for i in range(len(os.listdir(resld.resfol+"/media/prlx"))):
		print(f" - {i}")
		prlx=resld.load(f"{resld.resfol}/media/prlx/prlx{i+1}.png")
		if prlx.get_size() == (1920,1080):
			if prlx.get_size() != display.get_size():
				prlx = pg.transform.scale(prlx, display.get_size())
		else:
			prlx = pg.transform.scale(prlx, (prlx.get_width()/2, prlx.get_height()/2))
		prlxs[i+1]=prlx
	print(" - prlx1")
	prlx1=resld.load(f"{resld.resfol}/media/prlx/prlx1.png")
	prlx1 = pg.transform.scale(prlx1, (prlx1.get_width()/2, prlx1.get_height()/2))
	print(" - bge")
	bge=pg.Surface([bg.get_width(),prlxs[1].get_height()])
	bge.blit(bg, [0,0], [0,bg.get_height()-prlxs[1].get_height(),bg.get_width(),prlxs[1].get_height()])
	print(" - prlxw")
	prlxw=prlx1.get_width()
	print("Rendering Logotxt")
	logotxt = resld.render(fsm.gm[0])
	print("engine: reload compelete.")
	load_done = 1

## Game loop
while (running):
	sfx.dvol = fsm.get("Settings/volume/mastervolume")
	old_dt = dt
	dt = time.time()
	delta = (dt - old_dt) * fsm.get('Settings/game/pacing')
	if delta > 9:
		delta=0.1
	if ticks > 999999:
		ticks = 0
	if fticks > 999999:
		ticks = 0
	
	try:
		if data["LU"] != fsm.get('Settings/region/language'):
			data["Lang"] = json.loads(open(f"{resld.resfol}/lang/{fsm.get('Settings/region/language')}.json").read())["content"]
			data["LU"] = fsm.get('Settings/region/language')
	except:
		pass
	event = pg.event.get()
	event_key = pg.key.get_pressed()

	if ekeng.Running != "":
		filesolmesg = f" (Running ({ekeng.Running}))"
	
	try:
		# Handle events & keypresses/holds
		latest = 0
		for i in event:
			try:
				ev="pg_event"
				ekl.run(f"{resld.resfol}/data/scripts/event/{ev}.sol", gl=globals(), lc=locals())
			except:
				print("Event error")
			if i.type == pg.QUIT:
				running = 0
				print("quit")
				try:
					ev="gm_close"
					ekl.run(f"{resld.resfol}/data/scripts/event/{ev}.sol", gl=globals(), lc=locals())
				except:
					print("Event error")
			elif i.type == pg.WINDOWENTER:
				bgr=1
			elif i.type == pg.KEYDOWN:
				try:
					ev="k_keydown"
					ekl.run(f"{resld.resfol}/data/scripts/event/{ev}.sol", gl=globals(), lc=locals())
				except:
					print("Event error")
				for k in fsm.get("Settings/keys"):
					if fsm.get(f"Settings/keys/{k}/key") == pg.key.name(i.key) and not fsm.get(f"Settings/keys/{k}/holdable"):
						try:
							ekl.run(f"{resld.resfol}/data/scripts/key/{k}.sol", gl=globals(),lc=locals())
						except Exception as e:
							print(f"Key errors {e}")
				try:
					latest_key = pg.key.name(i.key)
				except:
					pass
			elif i.type == pg.KEYUP:
				try:
					ev="k_keyup"
					ekl.run(f"{resld.resfol}/data/scripts/event/{ev}.sol", gl=globals(), lc=locals())
				except:
					print("Event error")
			latest=pg.event.event_name(i.type)
		
		for k in fsm.get("Settings/keys"):
			ke = fsm.get(f"Settings/keys/{k}/key")
			if event_key[pg.key.key_code(ke)]:
				try:
					if fsm.get(f"Settings/keys/{k}/holdable"):
						ekl.run(f"{resld.resfol}/data/scripts/key/{k}.sol", gl=globals(),lc=locals())
				except Exception as e:
					print(f"Key errors {e}")
				try:
					latest_key = pg.key.name(i.key)
				except:
					pass
		
		# Loading
		if loadscr == 1:
			if fsm.get("Settings/load/splash") != "":
				setdisp(1,resolution=resld.load(f"{resld.resfol}/{fsm.get('Settings/load/splash')}.png"))
				loadscr=0.9
				if not loading and not (loadno or loadskp):
					sfx.play(resld.load(f"{resld.resfol}/media/load.mp3"),cc="load.mp3", volume=0.2)
					try:
						playersheet = resld.sheet(playermod["file"])
					except:
						print("Game errors load player")
					loadthread = threading.Thread(target=resld.load_all, name="LoadingScreen-Resource-Loader")
					loadb = threading.Thread(target=_load_all_eng, name="LoadingScreen-Engine")
					print("game: Loading Resources...")
					loadb.run()
					print("RT")
					loadthread.run()
					loading = 1
				
				if loadno or loadskp:
					sfx.play(resld.load(f"{resld.resfol}/media/load.mp3"),cc="load.mp3", volume=0.2)
					loadscr=0.9
					loading=0
					ldt = 1
				
				if resld.ldone:
					if ldt < fsm.get("Settings/load/lddelay"):
						ldt += delta
					else:
						loadscr = 0.5
						loading = 0
						ldt = 1
						print("game: Loading Complete!")
			else:
				ux.blit(resld.load(f"{resld.resfol}/media/eklips/ring.png"), [0,0], scale=2, anchor="cx cy",rotation=fticks*100)
				ux.blit(resld.load(f"{resld.resfol}/media/eklips/eklips.png"), [0,0], scale=2, anchor="cx cy",add_bg=0)
				try:
					if fsm.get("Settings/load/showtips"):
						ux.blit(resld.render(data["Lang"]["tip1"]), [0,190], scale=0.75, anchor="cx cy",add_bg=1)
					else:
						ux.blit(resld.render(data["Lang"]["load"]), [0,170], anchor="cx cy",add_bg=1)
				except:
					pass	
				if not loading and not (loadno or loadskp):
					sfx.play(resld.load(f"{resld.resfol}/media/load.mp3"),cc="load.mp3")
					try:
						playersheet = resld.sheet(playermod["file"])
					except:
						print("Game errors load player")
					loadthread = threading.Thread(target=resld.load_all, name="LoadingScreen-Resource-Loader")
					loadb = threading.Thread(target=_load_all_eng, name="LoadingScreen-Engine")
					print("game: Loading Resources...")
					loadb.run()
					loadthread.run()
					loading = 1
				
				if loadno or loadskp:
					sfx.play(resld.load(f"{resld.resfol}/media/load.mp3"),cc="load.mp3")
					loadscr=0.5
					loading=0
					ldt = 1

				if resld.ldone:
					if ldt < fsm.get("Settings/load/lddelay"):
						ldt += delta
					else:
						loadscr = 0.5
						loading = 0
						ldt = 1
						print("game: Loading Complete!")
		elif loadscr == 0.9:
			path = f"{resld.resfol}/{fsm.get('Settings/load/splash')}.png"
			print(path)
			ux.blit(resld.load(path), [0,0])
			ldt -= delta * 2
			if ldt < 0.1:
				loadscr = 0
				ldt = 0
				ldts = 1
				flags = 0
				loadskp=1
				resolution=fsm.get("Settings/display/res","full")
				setdisp(resolution)
		elif loadscr == 0.5: #LoadingFadeOut
			ux.blit(resld.load(f"{resld.resfol}/media/eklips/ring.png"), [0,0], scale=2, anchor="cx cy",rotation=fticks*100,alpha=ldt)
			ux.blit(resld.load(f"{resld.resfol}/media/eklips/eklips.png"), [0,0], scale=2, anchor="cx cy", alpha=ldt,add_bg=0)
			try:
				if fsm.get("Settings/load/showtips"):
					ux.blit(resld.render(data["Lang"]["tip1"]), [0,190], scale=0.75, anchor="cx cy",add_bg=1)
				else:
					ux.blit(resld.render(data["Lang"]["load"]), [0,170], anchor="cx cy",add_bg=1)
			except:
				pass	
			ldt -= delta * 2
			if ldt < 0.1:
				if not loadskp:
					loadscr = 0.25
				else:
					loadscr = 0
				ldt = 0
				ldts = 1
				loadskp=1
		elif loadscr == 0.25:
			#Developer credit
			ldt += delta * 2 * ldts
			if ldt > 1 and ldts == 1:
				ldts = -1
			elif ldt < 0 and ldts == -1:
				loadscr = 0
				ldt = 0
				ldts = 1
			
			ux.blit(resld.load(f"{resld.resfol}/media/gdev.png"), [0,0], scale=2, anchor="cx cy", alpha=ldt)
		else: # Script-based menu
			if data["Engine"]["MainMenu"]:
				if "bg" in fsm.get("Settings/performance"):
					if fsm.get("Settings/performance/bg"):
						if fsm.get("Settings/performance/prlx"):
							if bgr:
								ux.blit(bg, [0,0], add_bg=0, layer=2)
								bgr=0
							if not "Parallax" in data:
								data["Parallax"]={}
								for i in prlxs:
									data["Parallax"][i]=0

							if oldprlx != int(data["Parallax"][1]):
								if not bgr:
									ux.blit(bge, [0,0], add_bg=0, anchor="bottom", layer=2)
								
								prlxa=2
								prlxi=len(prlxs)
								for i in range(prlxi):
									prlxx=0
									for e in range(prlxa):
										if not bgr:
											ux.blit(bg, [data["Parallax"][i+1]+prlxx,0], clip=[data["Parallax"][i+1]+prlxx,0, prlxs[i+1].get_size()[0],prlxs[i+1].get_size()[1]], add_bg=0, anchor="bottom", layer=-70)
										ux.blit(prlxs[i+1], [data["Parallax"][i+1]+prlxx,0], anchor="bottom", add_bg=0, layer=-53+(i+1))
										prlxx+=prlxs[i+1].get_width()
								oldprlx = int(data["Parallax"][1])
							
							for i in data["Parallax"]:
								if data["Parallax"][1] < -prlxw/2:
									data["Parallax"][i] = -i
								data["Parallax"][i]-=i
						else:
							if bgr:
								if fsm.get("Settings/performance/bg") == "cblack":
									display.fill("black")
								else:
									ux.blit(bg, [0,0], add_bg=0, layer=2)
									bgr=0
				ekl.run(f"{resld.resfol}/data/scenes/script/{data['Engine']['Scene']}.sol",gl=globals(),lc=locals())
			else:
				ekl.run(f"{resld.resfol}/data/scripts/{fsm.get("Settings/private/UpdateScript")}.sol",gl=globals(),lc=locals())
		
			ticks += delta
		if solcons.bgr and not bgr:
			bgr=solcons.bgr
			solcons.bgr=0
		
		cmdpop = []
		for i in solcons.cmd:
			txtd=solcons.cmd[i]
			try:
				ekl.run(f"{resld.resfol}/data/scripts/cmd/{txtd[0]}.sol", gl=globals(),lc=locals())
			except Exception as e:
				solcons.text += f"Error running script: {e}\n"
			cmdpop.append(i)
		
		for i in cmdpop:
			solcons.cmd.pop(i)

		clock.tick(fsm.get("Settings/performance/Framerate"))
		Framerate=clock.get_fps()
		solcons.blit(event)

		if GCT > 1:
			gc.collect()
			GCT = 0
		GCT+=delta
		fps_text = resld.render(f"{round(Framerate)} FPS, {round(psutil.Process().memory_info().rss / 1024**2)}",cache=0)
		ux.blit(fps_text,[0,0], layer=4, add_bg=1, anchor="bottom")
		ux.render(fsm.get("Settings/display/FUNMODE"),alpha=rendalpha,enginealphasupport=fsm.get("Settings/private/SupportsAlpha"))
		ux.IncludeDebugOverlays = 1
		if gpumode:
			pg.display.flip()
		else:
			pg.display.update()
		ux.tick()
		fticks += delta
	except Exception as error:
		running = 0
		fsm.save_dat()
		pg.quit()
		ekhl.error(sol_ver, error, ekeng.Running)

pg.quit()
fsm.close()
fsm.save_dat()
