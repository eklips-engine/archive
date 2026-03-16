Sol.UI.blit(Sol.Resource.load(f"{Sol.Resource.resfol}/media/icon.png"), [50,50], size=(150,150))
Sol.UI.blit(Sol.Resource.render(Sol.Data["Lang"]["mstg"]), [250,100], scale=2, alpha=2)

catx=0
caty=25
catya=0
settings=Sol.Save.val("Settings")
try:
	settingsdata = Sol.ReadProp(f"{Sol.Resource.resfol}/Sol.Data/scenes/settings.sol")["info"]
except:
	settingsdata = {}

frame=Sol.UI.frame((Sol.Display.get_width()-50, Sol.Display.get_height()-350), [0, 250], anchor="cx", id="settings", sxs=3)
for category in settings:
	Sol.UI.blit(Sol.Resource.render(Sol.Data["Lang"]["opt-cat"][category], color="black"), [catx, caty+catya], scale=2, anchor="cx", disp=frame)
	
	opty=0
	for option in settings[category]:
		opos = [catx+75, 100+caty+opty]
		settingdata = {}
		value = settings[category][option]
		try:
			for info in settingsdata[option].split():
				optdat=info.split("/")
				settingdata[optdat[0]]=optdat[1]
		except:
			settingdata["type"] = "bool"
		
		optn=Sol.Data["Lang"]["opt"][option]
		Sol.UI.blit(Sol.Resource.render(optn, color="black"), opos, disp=frame)
		
		; Pretty janky way to fix this but it works sooo
		opos = [catx+75, 100+caty+opty]
		opos[1] += Sol.UI.frames[frame["AvailabilityCheckIsFrameObject"]]["y"]
		
		typec=Sol.ReadProp(f"{Sol.Resource.resfol}/Sol.Data/scripts/setting_type/{settingdata['type']}.sol")["info"]
		print(typec)
		txt="Unk"
		try:
			if "slider" in typec:
				setting=Sol.UI.slider(opos, value=value, min=int(settingdata["min"]), max=int(settingdata["max"]), disp=frame, anchor="right")
				
				if setting[0]:
					Sol.Save.set(f"Settings/{category}/{option}", setting[1])
			else:
				Sol.Execute(f"txt={typec['txt']}", isf=0, gl=globals(),lc=locals())
				setting=Sol.UI.button(Sol.Resource.render(txt, color="black"), opos, anchor="right", disp=frame)
				if setting:
					Sol.Execute(typec["code"], isf=0, gl=globals(),lc=locals())
		except Exception as e:
			setting=Sol.UI.button(Sol.Resource.render(e, color="red"), opos, anchor="right", disp=frame)
		
		opty+=50
	
	caty+=opty+75
	catya=25