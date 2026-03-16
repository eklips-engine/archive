#Filesystem and save manager
import os, json, shutil, threading, zipfile
import binascii

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
	return result

class Filesystem:
	def __init__(self, NAME):
		self.gm = NAME
		"""Filesystem and Save Manager"""
		self.zadir = f"{os.path.expanduser('~')}/Eklips Engine"
		self.pbdir = f"{self.zadir}/{NAME[0]}"
		self.savedir = f"{self.pbdir}/Saves"
		
		if not os.path.isdir(self.zadir):
			os.mkdir(self.zadir)
		if not os.path.isdir(self.pbdir):
			os.mkdir(self.pbdir)
			os.mkdir(self.savedir)
			os.mkdir(f"{self.savedir}/Backups")
		
		self.savedef = f"{NAME[1]}/default_save.json"
		self.savebak = f"{self.savedir}/Backups/save.json"
		self.save = f"{self.savedir}/save.json"
		self.sfile = {}
		self.load()
	
	def get(self, key, default=0):
		"""Get a key's value,
		KEY = key (duh),
		DEFAULT (OPTIONAL) = Default value when KEY is not found"""
		value = {"self": self, "val": default}
		newline="\n"
		code = f"val = self.sfile{path_to_list(key)}"
		try:
			exec(code, value)
		except:
			pass
		return value["val"]
	
	def set(self, val, out):
		"""Set a value, VAL is the key to set, and OUT is the value to set to VAL. Got that? Nope? Too bad."""
		oute=out
		if type(oute).__name__ == "str":
			oute=f'"{out}"'
		code=f"self.sfile{path_to_list(val)} = {oute}"
		print(code)
		exec(code, locals())
	
	def load(self):
		"""Load the savefile"""
		try:
			self.sfile = json.loads(open(self.save).read())
			with open(self.savebak, "w") as f:
				f.writelines(json.dumps(self.sfile, indent=1))
			print("WriteSafeBak")
		except:
			if self.savebak in os.listdir(self.savedir):
				self.sfile = json.loads(open(self.savebak).read())
				self.save_dat()
				print("UseBak")
			else:
				try:
					self.sfile = json.loads(open(self.savedef).read())
				except:
					self.sfile = {}
				self.save_dat()
				print("ResetSave")
			self.save_dat()
		
	def close(self):
		"""Save all data... 5 times. Just to make sure"""
		self.save_dat()

	def save_dat(self):
		"""Save all data... 5 times. Just to make sure"""
		for i in range(5):
			with open(self.save, "w") as f:
				f.writelines(json.dumps(self.sfile, indent=1))
			with open(self.savebak, "w") as f:
				f.writelines(json.dumps(self.sfile, indent=1))

if __name__ == "__main__":
	fsm=Filesystem()
	fsm.convert(input("Convert: "))
	fsm.save_dat()