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
	def __init__(self, game="SolRedist\nsol"):
		"""Filesystem and Save Manager"""
		self.zadir = f"{os.path.expanduser('~')}/Za9118"
		self.gmdir = f"{self.zadir}/{game[0]}"
		self.savedir = f"{self.gmdir}/Saves"
		
		if not os.path.isdir(self.zadir):
			os.mkdir(self.zadir)
		if not os.path.isdir(self.gmdir):
			os.mkdir(self.gmdir)
			os.mkdir(self.savedir)
			os.mkdir(f"{self.savedir}/Backups")
		
		self.savedef = f"{game[1]}/data/Saves/Default.json"
		self.savebak = f"{self.savedir}/Backups/save.json"
		self.save = f"{self.savedir}/save.json"
		
		self.fsbak = f"{self.savedir}/Backups/filesystem.json"
		self.fs = f"{self.savedir}/fs.json"
		
		self.fsfile = {}
		self.sfile = {}
		self.load()
		self.cd = "/"
	
	def val(self, key):
		value = {"self": self, "val": 0}
		newline="\n"
		exec(f"val = self.sfile{path_to_list(key)}", value)
		return value["val"]
	
	def set(self, val, out):
		exec(f"self.sfile{path_to_list(val)} = {out}", locals())
	
	def load(self):
		try:
			self.sfile = json.loads(open(self.save).read())
			with open(self.savebak, "w") as f:
				f.writelines(json.dumps(self.sfile, indent=1))
		except:
			if self.savebak in os.listdir(self.savedir):
				self.sfile = json.loads(open(self.savebak).read())
				self.save_dat()
			else:
				self.sfile = json.loads(open(self.savedef).read())
				self.save_dat()
		
	def save_dat(self):
		with open(self.save, "w") as f:
			f.writelines(json.dumps(self.sfile, indent=1))
		with open(self.savebak, "w") as f:
			f.writelines(json.dumps(self.sfile, indent=1))
		
		self.load()
	
if __name__ == "__main__":
	fsm=Filesystem()
	fsm.convert(input("Convert: "))
	fsm.save_dat()