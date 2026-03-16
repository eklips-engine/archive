Sol.UI.blit(Sol.Resource.load(f"{Sol.Resource.resfol}/media/icon.png"), [50,50], size=(150,150))
Sol.UI.blit(Sol.Resource.render(Sol.Data["Lang"]["mexit"]), [250,100], scale=2, alpha=2)
Sol.UI.blit(Sol.Resource.render(Sol.Data["Lang"]["mexit1"]), [50,225], alpha=2)

y=Sol.UI.button(Sol.Resource.render(Sol.Data["Lang"]["yes"]), [100,300], alpha=2)
n=Sol.UI.button(Sol.Resource.render(Sol.Data["Lang"]["no"]), [100,350], alpha=2)
if y:
	Sol.Engine.IsRunning=0
if n:
	Sol.Data["Engine"]["Transition"] = "main?"