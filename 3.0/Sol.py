## Import
import pygame as pg
import tkinter
import traceback, threading
import solhl
import classes.overlay as overlay
from tkinter.messagebox import *
import os, time, json, threading, random, requests
from classes import res, fs, ui, sfxsys, kink, soleng, network as net
from classes.overlay import console, achievement, _overlay

## Init
pg.init()

## Display
display_size = pg.display.get_desktop_sizes()[0]
flags = pg.FULLSCREEN
display = pg.display.set_mode(display_size, flags)

## Caption
pg.display.set_caption(open("game.txt").read().splitlines()[0])

## Clock
clock = pg.time.Clock()

## Filesystem
fsm = fs.Filesystem(open("game.txt").read().splitlines())

## RescLoader
resfol=open("game.txt").read().splitlines()[1]
resld = res.ResourceLoader(resfol)

## Icon
try:
	pg.display.set_icon(resld.load(f"{resld.resfol}/media/icon.png"))
except:
	pg.display.set_icon(resld.load(f"{resld.resfol}/media/sol/icon.png"))

## SoundSystem
sfx = sfxsys.SoundSystem()

## User Interface
ux = ui.Interface(display, sfx, resld.load(f"{resld.resfol}/media/click.mp3"), resld)

## KinkReader
kinkr = kink.KinkVid(ux, resld)

## Sol related
sol_ver = open(f"{resld.resfol}/ver.txt").read().splitlines()[1]
sol = soleng.Engine()
solengi = sol
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
			"File": "lvl1"
		}
	},
	
	"Lang": json.loads(open(f"{resld.resfol}/lang/{fsm.val('Settings/region/language')}.json").read())["content"],
	"Debug": 1
}

def servref(ip=""):
	e=net.ServerList(ip)
	return e.out

servers={}

## Loader
loadscr = 1
loadthread = None
loading = 0
ldt = 0
ldts = 1
loadskp = fsm.val("Settings/load/loadskip")
loadno = fsm.val("Settings/load/noload")

## InstancePlayer properties
try:
	playermod = sol.read(f"{resld.resfol}/data/instances/player.sol")["info"]
except:
	print("Sol playermod gone, game errors expected")

## Spritesheet
try:
	playersheet = resld.sheet(playermod["file"])
except:
	print("Sol playersheet gone, game errors expected")

## Menu assets
bg = resld.load(resld.resfol+"/media/bg.png")
logotxt = resld.render(fsm.gm)

try:
	ev="start"
	sol.run(f"{resld.resfol}/data/scripts/event/{ev}.sol", gl=globals(), lc=locals())
except:
	print("Event error")

## Game loop
while (running):
	old_dt = dt
	dt = time.time()
	delta = dt - old_dt
	
	event = pg.event.get()
	event_key = pg.key.get_pressed()
	display.fill("black")
	
	try:
		# Handle events & keypresses/holds
		latest = 0
		for i in event:
			try:
				ev="pg_event"
				sol.run(f"{resld.resfol}/data/scripts/event/{ev}.sol", gl=globals(), lc=locals())
			except:
				print("Event error")
			if i.type == pg.QUIT:
				running = 0
				print("quit")
				try:
					ev="gm_close"
					sol.run(f"{resld.resfol}/data/scripts/event/{ev}.sol", gl=globals(), lc=locals())
				except:
					print("Event error")
			elif i.type == pg.KEYDOWN:
				try:
					ev="k_keydown"
					sol.run(f"{resld.resfol}/data/scripts/event/{ev}.sol", gl=globals(), lc=locals())
				except:
					print("Event error")
				print(f"keypress {pg.key.name(i.key)}")
				for k in fsm.val("Settings/keys"):
					if fsm.val(f"Settings/keys/{k}") == pg.key.name(i.key):
						try:
							sol.run(f"{resld.resfol}/data/scripts/key/{k}.sol", gl=globals(),lc=locals())
						except:
							print("Key errors")
				try:
					latest_key = pg.key.name(i.key)
				except:
					pass
			elif i.type == pg.KEYUP:
				try:
					ev="k_keyup"
					sol.run(f"{resld.resfol}/data/scripts/event/{ev}.sol", gl=globals(), lc=locals())
				except:
					print("Event error")
				print(" | keyup")
			else:
				print(f"event: {pg.event.event_name(i.type)}")
			latest=pg.event.event_name(i.type)
		
		for k in fsm.val("Settings/keys"):
			ke = fsm.val(f"Settings/keys/{k}")
			if event_key[pg.key.key_code(ke)]:
				try:
					sol.run(f"{resld.resfol}/data/scripts/key/{k}.sol", gl=globals(),lc=locals())
				except:
					print("Key errors")
				try:
					latest_key = pg.key.name(i.key)
				except:
					pass
		
		# Loading
		if loadscr == 1:
			if loadno or loadskp:
				loadscr=0
			
			ux.blit(resld.load(f"{resld.resfol}/media/sol/sol.png"), [0,0], scale=2, anchor="cx cy")
			ux.blit(resld.load(f"{resld.resfol}/media/sol/ring.png"), [0,0], rotation=fticks*100, scale=2, anchor="cx cy")
			if fsm.val("Settings/load/showtips"):
				ux.blit(resld.render(data["Lang"]["tip1"]), [0,190], scale=0.75, anchor="cx cy")
			else:
				ux.blit(resld.render(data["Lang"]["load"]), [0,170], anchor="cx cy")
			
			if not loading:
				sfx.play(resld.load(f"{resld.resfol}/media/load.mp3"))
				try:
					playersheet = resld.sheet(playermod["file"])
				except:
					print("Game errors load player")
				loadthread = threading.Thread(target=resld.load_all, name="LoadingScreen-Resource-Loader")
				print("game: Loading Resources...")
				loadthread.run()
				loading = 1
			
			if resld.ldone:
				if ldt < fsm.val("Settings/load/lddelay"):
					ldt += delta
				else:
					loadscr = 0.5
					loading = 0
					ldt = 1
		elif loadscr == 0.5: #LoadingFadeOut
			ux.blit(resld.load(f"{resld.resfol}/media/sol/sol.png"), [0,0], scale=2, anchor="cx cy", alpha=ldt)
			ux.blit(resld.load(f"{resld.resfol}/media/sol/ring.png"), [0,0], rotation=fticks*100, scale=2, anchor="cx cy", alpha=ldt)
			ux.blit(resld.render(delta), [0,170], anchor="cx cy", alpha=ldt)
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
			
			ux.blit(resld.load(f"{resld.resfol}/media/gdev.png"), [0,5], scale=2, anchor="cx cy", alpha=ldt)
		else: # Built-in menu
			if data["Engine"]["MainMenu"]:
				if "bg" in fsm.val("Settings/peformance"):
					if fsm.val("Settings/peformance/bg"):
						if fsm.val("Settings/peformance/prlx"):
							ux.blit(bg, [0,0], scale=3, anchor="cx cy")
						else:
							ux.blit(bg, [0,0], scale=3, anchor="cx cy")
					
				try:
					sol.run(f"{resld.resfol}/data/scenes/script/{data['Engine']['Scene']}.sol",gl=globals(),lc=locals())
				except:
					ux.blit(resld.load(f"{resld.resfol}/media/icon.png"), [50,50], size=(150,150))
					ux.blit(resld.render(data["Lang"]["munk"]), [250,100], scale=2, alpha=2)
					
					ux.blit(resld.render(data["Lang"]["munk1"]), [50,250], alpha=2)
					
				if not data["Engine"]["Scene"] in ["main", "int2"]:
					back = ux.button(resld.render(data["Lang"]["back"]), [25,25], anchor="bottom")
					if back:
						data["Engine"]["Transition"] = "main?"
			else: # Game
				## Player
				if data["Engine"]["Player"]["Vel"][0]:
					ux.blit(playersheet[1], [0,85], scale=10, anchor="cx cy", clip=playersheet[0]["Body"]["w"+str(round(data["Engine"]["GameAnimSpeed"]))], flip=data["Engine"]["Player"]["Flp"])
				else:
					ux.blit(playersheet[1], [0,85], scale=10, anchor="cx cy", clip=playersheet[0]["Body"]["i1"], flip=data["Engine"]["Player"]["Flp"])
				
				ux.blit(resld.load(f"{resld.resfol}/media/null.png"), [0,0], scale=.5, anchor="cx cy", rotation=-45)
				
				ux.blit(playersheet[1], [0,0], scale=10, anchor="cx cy", clip=playersheet[0]["Head"][str(round(data["Engine"]["GameAnimSpeed"]))], flip=data["Engine"]["Player"]["Flp"])
				
				## Movement & Gravity
				data["Engine"]["Player"]["Pos"][0] += data["Engine"]["Player"]["Vel"][0]
				data["Engine"]["Player"]["Pos"][1] += data["Engine"]["Player"]["Vel"][1]
				data["Engine"]["Player"]["Vel"][1] -= (int(playermod["gravity"]) * 10) * delta
				
				## Tick
				data["Engine"]["GameAnimSpeed"] += delta * 6
				if data["Engine"]["GameAnimSpeed"] > 4:
					data["Engine"]["GameAnimSpeed"]=1
			
			if data["Engine"]["Transition"] != "":
				if "?" in data["Engine"]["Transition"]:
					tid = data["Engine"]["Transition"].replace("?", "")
					tn = data["Lang"].get("m"+tid)
					
					if tid == "main":
						tn = fsm.gm
					
					if data["Engine"]["TAF"] > 2 and data["Engine"]["TAlpha"] > 100:
						data["Engine"]["Scene"] = tid
						data["Engine"]["TAlpha"] = 0
						data["Engine"]["TAF"] = 1
						data["Engine"]["Transition"]=""
					
					ts=6
					data["Engine"]["TAF"]+=(2/4)*delta*ts
					if data["Engine"]["TAF"] > 2:
						data["Engine"]["TAF"]=2.1
					
					mainmenudat=sol.read(f"{resld.resfol}/data/scenes/mainmenu.sol")["info"]
					
					opty=0
					o=0
					if mainmenudat["menu_anchor"]=="":
						opty=275
					for i in mainmenudat["options"].split("_"):
						dat=i.split("/")
						if not dat[0].lstrip("m") == tid:
							o+=50
						else:
							break
					
					pos=[50+int(100*(data["Engine"]["TAF"])),opty-int((data["Engine"]["TAlpha"]-1)*(87.5))+o+data["Engine"]["TAF"]]
					data["Engine"]["TAlpha"]+=2*delta*ts
					if pos[1] < 100:
						pos[1]=100.1
						data["Engine"]["TAlpha"] = 100.1
					
					txt=resld.render(tn)
					ux.blit(txt, pos, scale=data["Engine"]["TAF"], alpha=200)
				else:
					if data["Engine"]["TAlpha"] < 1 and data["Engine"]["TSpeed"] == -1:
						data["Engine"]["TAlpha"]=0
						data["Engine"]["TSpeed"]=1
						data["Engine"]["Transition"]=""
					if data["Engine"]["TAlpha"] > 0.75 and data["Engine"]["TSpeed"] == 1:
						data["Engine"]["Scene"] = data["Engine"]["Transition"]
						data["Engine"]["TSpeed"] = -1
					data["Engine"]["TAlpha"]+=data["Engine"]["TSpeed"]*(2*delta)
					ux.fill((0,0,0), alpha=data["Engine"]["TAlpha"])
					data["Engine"]["TAF"]+=delta*6
					if data["Engine"]["TAF"] > 4:
						data["Engine"]["TAF"]=1
					
					ux.blit(playersheet[1], [0,0], alpha=data["Engine"]["TAlpha"], scale=10, anchor="cx cy", clip=playersheet[0]["Head"][str(round(data["Engine"]["TAF"]))])
			
			ticks += delta
		
		cmdpop = []
		for i in solcons.cmd:
			txtd=solcons.cmd[i]
			try:
				sol.run(f"{resld.resfol}/data/scripts/cmd/{txtd[0]}.sol", gl=globals(),lc=locals())
			except:
				solcons.text += "Error\n"
			cmdpop.append(i)
		
		for i in cmdpop:
			solcons.cmd.pop(i)
		
		solcons.draw(event)
		pg.display.flip()
		ux.tick()
		clock.tick(fsm.val("Settings/peformance/fps"))
		fticks += delta
	except Exception as error:
		running = 0
		pg.quit()
		solhl.error(sol_ver, error)

pg.quit()
fsm.save_dat()
if fsm.getfile() != fsm.sfile:
	with open(fsm.save, "w") as f:
		f.writelines(json.dumps(fsm.sfile))
	print("ExtraSave: done")