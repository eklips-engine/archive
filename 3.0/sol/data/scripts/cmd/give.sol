fn usage():
	Sol.Console.text += "Usage: give <item>\n"

try:
 if Sol.Data["Engine"]["CVar"]["cheats"]:
  Sol.Data<Player>["Inventory"].append(txtd[1])
  Sol.Console.text += f"Gave player {txtd[1]}"
except:
	usage()