fn usage(e=0):
	Eklips.Console.printf(f"Error {e}\n")

try:
	fsm = fs.Filesystem(open("game.txt").read().splitlines())
	loadscr = 1
	loadthread = None
	loading = 0
	ldt = 0
	ldts = 1
	loadskp = fsm.get("Settings/load/loadskip")
	loadno = fsm.get("Settings/load/noload")
except Exception as e:
	usage(e)