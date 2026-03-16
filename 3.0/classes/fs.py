#Filesystem and save manager
import os, json, shutil, threading

def list_files_first(path="."):
	items = os.listdir(path)
	files = [item for item in items if os.path.isfile(os.path.join(path, item))]
	directories = [item for item in items if os.path.isdir(os.path.join(path, item))]
	files.sort()
	directories.sort()
	return files + directories

x=0
def path_to_list(path):
	path_list = path.split("/")
	result = ""
	for segment in path_list:
		result += f'["{segment.strip("/")}"]'
	return result
	
def get_dir_before(path):
	path_list = path.split("/")
	result = "/".join(path_list[:-1]).lstrip("/")
	return result

def get_last_item(path):
	path_list = path.split("/")
	result = path_list[-1].lstrip("/")
	print(result)
	return result

class Filesystem:
	def __init__(self, game=["SolRedist", "sol"]):
		"""Filesystem and Save Manager"""
		self.zadir = f"{os.path.expanduser('~')}/Sol Engine"
		self.gmdir = f"{self.zadir}/{game[0]}"
		self.gm=game[0]
		self.savedir = f"{self.gmdir}/Saves"
		
		if not os.path.isdir(self.zadir):
			os.mkdir(self.zadir)
		if not os.path.isdir(self.gmdir):
			os.mkdir(self.gmdir)
			os.mkdir(self.savedir)
			os.mkdir(f"{self.savedir}/Backups")
		
		self.savedef = f"{game[1]}/default_save.json"
		self.savebak = f"{self.savedir}/Backups/save.json"
		self.save = f"{self.savedir}/save.json"
		
		self.fsbak = f"{self.savedir}/Backups/filesystem.json"
		self.fs = f"{self.savedir}/fs.json"
		
		self.fsfile = {}
		self.sfile = {}
		self.load()
		self.cd = "/"
	
	def getfile(self):
		return json.loads(open(self.save).read())
	
	def val(self, key, default=0):
		value = {"self": self, "val": 0}
		newline="\n"
		try:
			exec(f"val = self.sfile{path_to_list(key)}", value)
		except:
			exec(f"self.sfile{path_to_list(key)} = {default}", value)
			value["val"] = default
		return value["val"]
	
	def set(self, val, out):
		exec(f"self.sfile{path_to_list(val)} = {out}", locals())
	
	def load(self):
		try:
			self.sfile = json.loads(open(self.save).read())
			print("Loaded savefile")
			with open(self.savebak, "w") as f:
				f.write(json.dumps(self.sfile, indent=1))
				print("Written backup")
		except:
			if self.savebak in os.listdir(self.savedir):
				self.sfile = json.loads(open(self.savebak).read())
				print("Loaded backup")
				self.save_dat()
				print("Saved backup->main")
			else:
				self.reset()
				print("Reset savefile")
	
	def reset(self):
		self.sfile = json.loads(open(self.savedef).read())
		self.save_dat()
	
	def save_dat(self):
		print("Saving..")
		with open(self.save, "w") as f:
			print(" | Opened file")
			f.write(json.dumps(self.sfile, indent=1))
			print(" | Save written")
		with open(self.savebak, "w") as f:
			print(" | Opened backup")
			f.write(json.dumps(self.sfile, indent=1))
			print(" | Backup written")
		
		self.load()
	
if __name__ == "__main__":
	print(__file__)
	fsm=Filesystem()
	fsm.convert(input("Convert: "))
	fsm.save_dat()