Sol.Data["Engine"]["Scene"] = "main"
Sol.Data["Engine"]["MainMenu"] = 0
try:
	ev="gm_open"
	sol.run(f"{resld.resfol}/data/scripts/event/{ev}.sol", gl=globals(), lc=locals())
except:
	print("Event error")