## Import
import pygame as pg
import os, time, json, threading, random
from classes import res, fs, ui, sfxsys, kink, soleng

## Init
pg.init()

## Display
display_size = pg.display.get_desktop_sizes()[0]
flags = pg.FULLSCREEN
display = pg.display.set_mode(display_size, flags)

## Clock
clock = pg.time.Clock()

## Filesystem
fsm = fs.Filesystem(open("game.txt").read().splitlines())

## RescLoader
resld = res.ResourceLoader(resfol=open("game.txt").read().splitlines()[1])

## SoundSystem
sfx = sfxsys.SoundSystem()

## User Interface
ux = ui.Interface(display, sfx, resld.load(f"{resld.resfol}/sfx/click.mp3"))

## KinkReader
kinkr = kink.KinkVid(ux, resld)

## Sol class
sol = soleng.SolWID()
solscript = f"{resld.resfol}/{resld.resfol}-script.wid"
solimage  = f"{resld.resfol}/{resld.resfol}-image.wid"

## Variables
running = 1
ticks = 1 # seconds in game
fticks = 0 # include loading

## Delta Time
old_dt = time.time()
dt = time.time()

## Game Data
data = {
	"Lang": json.loads(open(f"{resld.resfol}/data/Languages/{fsm.val('Settings/language')}.json").read())["content"],
	"Debug": 1
}

## Loader
loadscr = 1
loadthread = None
loading = 0
ldt = 0
ldts = 1
loadskp = fsm.val("Settings/loadskip")
loadno = fsm.val("Settings/noload")

## Game loop
while (running):
	old_dt = dt
	dt = time.time()
	delta = dt - old_dt
	
	display.fill("black")
	
	nofs = (not "/" in fsm.fsfile) #No Root Folder
	
	for i in pg.event.get():
		if i.type == pg.QUIT:
			running = 0
	try:
		if loadscr == 1: #Loading
			if loadno or loadskp:
				loadscr=0
			
			ux.blit(resld.load(f"{resld.resfol}/img/SolLogo/sol.png"), [0,0], scale=2, anchor="cx cy")
			ux.blit(resld.load(f"{resld.resfol}/img/SolLogo/ring.png"), [0,0], rotation=fticks*100, scale=2, anchor="cx cy")
			if fsm.val("Settings/showtips"):
				ux.blit(resld.render(data["Lang"]["tip1"]), [0,190], scale=0.75, anchor="cx cy")
			else:
				ux.blit(resld.render(data["Lang"]["load"]), [0,170], anchor="cx cy")
			
			if not loading:
				sfx.play(resld.load(f"{resld.resfol}/sfx/starthdd.mp3"))
				loadthread = threading.Thread(target=resld.load_all, name="LoadingScreen-Resource-Loader")
				loadthread.run()
				loading = 1
			
			if resld.ldone:
				if ldt < fsm.val("Settings/lddelay"):
					ldt += delta
				else:
					loadscr = 0.5
					loading = 0
					ldt = 1
		elif loadscr == 0.5: #LoadingFadeOut
			ux.blit(resld.load(f"{resld.resfol}/img/SolLogo/sol.png"), [0,0], scale=2, anchor="cx cy", alpha=ldt)
			ux.blit(resld.load(f"{resld.resfol}/img/SolLogo/ring.png"), [0,0], rotation=fticks*100, scale=2, anchor="cx cy", alpha=ldt)
			ux.blit(resld.render("doneLoading"), [0,170], anchor="cx cy", alpha=ldt)
			ldt -= 0.05
			if ldt < 0.1:
				if not loadskp:
					loadscr = 0.25
				else:
					loadscr = 0
				ldt = 0
				ldts = 1
				loadskp=1
		elif loadscr == 0.25: #Za credit
			ldt += 0.05 * ldts
			if ldt > 1 and ldts == 1:
				ldts = -1
			elif ldt < 0 and ldts == -1:
				loadscr = 0
				ldt = 0
				ldts = 1
				if fsm.val("Empty"):
					fsm.set("Empty", 0)
				sol.run(solscript, "main.sol")
			
			ux.blit(resld.load(f"{resld.resfol}/img/auth.png"), [0,5], scale=2, anchor="cx cy", alpha=ldt)
		else: # Game?
			ticks += delta
	except Exception as e:
		running = 0
		print(e)
		raise e
	
	pg.display.flip()
	ux.tick()
	clock.tick(60)
	fticks += delta

fsm.save_dat()