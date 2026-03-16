fn usage():
	Sol.Console.printf("Usage: give <item>\n")

try:
 if Sol.Data["Engine"]["CVar"].get("cheats"):
  Sol.Data<Player>["Inventory"].append(txtd[1])
  Sol.Console.printf(f"Gave player {txtd[1]}")
except Exception as e:
	usageee(e)