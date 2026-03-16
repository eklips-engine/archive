def lwt(data):
	out = "slvl\x00\x00"
	for i in data:
		out += "\x01"
		
		if i == "tile":
			out+="\xFA"
		elif i == "entity":
			out+="\xFB"
		else:
			out+="\xFC"
		
		for j in data[i]: #J=Item in data
			for k in data[i][j]:
				out+=str(data[i][j][k])
				out+="\x04"
			out+="\x03"
		
		out += "\x02"
	
	out += "\xFF"
	return out