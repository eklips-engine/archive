ux.blit(bg, [0,0], add_bg=0, layer=2)
for i in data["ObjectsUpd"]:
    data["ObjectsUpd"][i].update(Eklips.DT)
data["Engine"]["GameAnimSpeed"] += Eklips.DT * 6
if data["Engine"]["GameAnimSpeed"] > 4:
	data["Engine"]["GameAnimSpeed"]=1
