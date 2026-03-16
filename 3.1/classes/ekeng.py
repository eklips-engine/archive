import json, os
import threading as th

Running = {}

class Engine:
	# Sol tools
	def __init__(self):
		pass
	
	class Level:
		def __init__(self, file):
			self.file = file
		
		def read(self):
			res={
				"tile": {},
				"entity": {}
			}
			section="none"
			
			with open(self.file, "r") as f:
				magic = f.read(4)
				print(f"magic: {magic}")
				if magic.lower() == "slvl":
					while (1):
						chr = f.read(1)
						
						if chr == "\x01":
							secid = f.read(1)
							if secid == "\xFA":
								section="tile"
							elif secid == "\xFB":
								section="entity"
							elif secid == "\xFC":
								section="meta"
							print(f"section: {section}")
							tmp=""
							tmp1=""
							tmp2=""
							while (1):
								chr = f.read(1)
								if chr == "\x02":
									section="none"
									break
								elif chr == "\x03":
									tmp1=tmp.split("\x04")
									if section=="tile":
										tmp2={
											"obj_id": tmp1[0],
											"pos_x": tmp1[1],
											"pos_y": tmp1[2],
											"prp_scale": tmp1[3],
											"nbt_nbt": tmp1[4]
										}
										print(f" | Tile: [\n |  ObjectID={tmp2['obj_id']},\n |  Pos=({tmp2['pos_x']}, {tmp2['pos_y']}),\n |  Properties=[\n |     Scale={tmp2['prp_scale']},\n |     NBT={tmp2['nbt_nbt']}\n |  ]\n | ]")
									elif section=="entity":
										tmp2={
											"ent_id": tmp1[0],
											"pos_x": tmp1[1],
											"pos_y": tmp1[2],
											"prp_hp": tmp1[3],
											"prp_sm": tmp1[4],
											"prp_plr": tmp1[5],
											"nbt_nbt": tmp1[6]
										}
										print(f" | Entity: [\n |  EntityID={tmp2['ent_id']},\n |  Pos=({tmp2['pos_x']}, {tmp2['pos_y']}),\n |  Properties=[\n |     Health={tmp2['prp_hp']},\n |     Stamina={tmp2['prp_sm']},\n |     PlayerName={tmp2['prp_plr']},\n |     NBT={tmp2['nbt_nbt']}\n |  ]\n | ]")
									res[section][len(res[section])] = tmp2
									tmp=""
									tmp1=""
									tmp2=""
								else:
									tmp += chr
						elif chr == "\xFF":
							break
				else:
					print("Unknown file format")
				
			return res
		
	def run(self,file,isf=1,gl=0,lc=0):
		global Running
		id=file.replace("\\",".").replace("/",".")
		if isf:
			try:
				code=open(file).read()
			except:
				code=""
		else:
			code=file
		if not gl:
			gl = globals()
		if not lc:
			lc = locals()
		Running[id]=[gl,lc]
		
		superset=self.read(".ekeng/superset.sol")["info"]
		for i in superset:
			code=code.replace(i.rstrip(" "), superset[i].lstrip(" "))
		
		exec(code, gl, lc)
		Running.pop(id)
	
	def read(self,file):
		#Read Sol config files
		res={"type": None, "info": {}}
		data=open(file).read()
		for i in data.splitlines():
			if i.startswith("@"):
				res["type"] = i.lstrip("@")
			else:
				res["info"][i.split("=")[0]]=i.split("=")[1]
		return res

if __name__ == "__main__":
	eng=Engine()
	print(__file__)