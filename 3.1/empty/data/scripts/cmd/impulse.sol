if txtd[1] == "100":
    fsm.set("Settings/display/FUNMODE", 1)
if txtd[1] == "101":
    fsm.set("Settings/display/FUNMODE", 0)
if txtd[1] == "90":
    data['Engine']['Scene'] = "main"