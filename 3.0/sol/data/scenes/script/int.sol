try:
	mainmenudat=Sol.ReadProp(f"{Sol.Resource.resfol}/Sol.Data/scenes/mainmenu.sol")["info"]
	intdat = Sol.ReadProp(f"{Sol.Resource.resfol}/Sol.Data/scenes/multiplayer.sol")["info"]["options"]
except:
	mainmenudat={"menu_anchor": ""}
	intdat=""

Sol.UI.blit(Sol.Resource.load(f"{Sol.Resource.resfol}/media/icon.png"), [50,50], size=(150,150), alpha=2)
Sol.UI.blit(Sol.Resource.render(Sol.Data["Lang"]["mint"]), [250,100], scale=2, alpha=2)

opty=0
if mainmenudat["menu_anchor"]=="":
	opty=275

for i in intdat.split("_"):
	dat = i.split("/")
	nm = Sol.Data["Lang"].get(dat[0])
	act=dat[1]
	
	option=Sol.UI.button(Sol.Resource.render(nm), [50,opty], anchor=mainmenudat["menu_anchor"])
	
	if option and Sol.Data["Engine"]["Transition"] == "":
		try:
			Sol.Execute(f"{Sol.Resource.resfol}/Sol.Data/scripts/menu_option/{act}.sol", gl=globals(),lc=locals())
		except:
			print("Multiplayer menu broken option")
	
	opty+=50