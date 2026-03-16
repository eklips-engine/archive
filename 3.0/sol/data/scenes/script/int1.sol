Sol.UI.blit(Sol.Resource.load(f"{Sol.Resource.resfol}/media/icon.png"), [50,50], size=(150,150), alpha=2)
Sol.UI.blit(Sol.Resource.render(Sol.Data["Lang"]["mint1"]), [250,100], scale=2, alpha=2)

frame=Sol.UI.frame((Sol.Display.get_width()-50, Sol.Display.get_height()-350), [0, 250], anchor="cx", id="Sol.Networking.ServersList")
sy=25

for server in Sol.Networking.Servers:
	sdat = Sol.Networking.Servers[server]
	Sol.UI.blit(Sol.Resource.render(sdat[0], color="black"), [25, sy], scale=2, disp=frame)
	Sol.UI.blit(Sol.Resource.render(f"{sdat[1]}, {sdat[2]} players", color="black"), [25, sy+57], scale=1, disp=frame)
	sy+=150

if len(Sol.Networking.Servers) == 0:
	Sol.UI.blit(Sol.Resource.render(Sol.Data["Lang"]["mempty"], color="black"), [0, 0], anchor="cx cy", scale=1, disp=frame)

refresh = Sol.UI.button(Sol.Resource.render(Sol.Data["Lang"]["mrefresh"]), [25,25], anchor="bottom right")
if refresh:
	Sol.Data["Engine"]["Transition"] = "int1.1"