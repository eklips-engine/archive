fn usage(e=0):
	Sol.Console.printf(f"Usage: run <file> {e}\n")

try:
 if Sol.Data["Engine"]["CVar"]["cheats"]:
  Sol.RunFile(txtd[1])
except Exception as e:
	usage(e)