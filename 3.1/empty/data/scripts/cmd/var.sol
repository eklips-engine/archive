try:
	if Sol.Networking.IsHost:
		try:
			Sol.Console.printf(f"{txtd[1]} = {txtd[2]}\n")
			Sol.Data["Engine"]["CVar"][txtd[1]] = txtd[2]
		except:
			Sol.Console.printf(f"{txtd[1]} = {Sol.Data['Engine']['CVar'].get(txtd[1])}\n")
except:
	try:
		Sol.Console.printf(f"{txtd[1]} = {txtd[2]}\n")
		Sol.Data["Engine"]["CVar"][txtd[1]] = txtd[2]
	except:
		Sol.Console.printf(f"{txtd[1]} = {Sol.Data['Engine']['CVar'].get(txtd[1])}\n")