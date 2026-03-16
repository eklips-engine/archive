## Sol Networking
import socket, threading, time, random
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *

class SocketObj:
	def __init__(self):
		self.ip = (0,0)
	
	def make(self, stfu=0):
		self.obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if not stfu:
			print("[SocketObj] make()")
		self.ip = (0,0)
	
	def bind(self, ip_port, stfu=0):
		if not stfu:
			print(f"[SocketObj/Server] bind({ip_port})")
		self.ip = ip_port
		
		while 1:
			try:
				self.obj.bind(self.ip)
				if not stfu:
					print(" |-> Found an available port! ")
				break
			except OSError:
				ip_port = list(ip_port)
				ip_port[1] = random.randint(1000,1200)
				self.ip = tuple(ip_port)
	
	def connect(self, ip_port, stfu=0):
		if not stfu:
			print(f"[SocketObj/Client] connect({ip_port})")
		self.obj.connect(ip_port)
	
	def listall(self, ip, debug=0):
		port=1000
		res = {}
		print(f"[SocketObj/ServerList] listall({ip}) = Searching...")
		while 1:
			strng = f"{port}/1200"
			try:
				self.connect((ip, port),stfu=1)
				self.send("/slist-data",stfu=1)
				sdata = self.recv(400,stfu=1)
				self.send("/close",stfu=1)
				res[f"{ip}:{port}"] = sdata
				self.obj.disconnect((ip, port))
			except:
				port+=1
				if port > 1200:
					break
		if debug:
			showinfo(f"Sol Networking", f"Ping Function Report:\n\n {len(res)} server(s) found.\n\n List: {res}")
		print(f"[SocketObj/ServerList] listall({ip}) = {res}")
		return res
	
	def listen(self, max=4, stfu=0):
		if not stfu:
			print(f"[SocketObj/Server] listen({max})")
		self.obj.listen(max)
	
	def recv(self, bit=1024, stfu=0):
		res=self.obj.recv(bit).decode()
		if not stfu:
			print(f"[SocketObj/Client] recv({bit}) = {res}")
		return res
	
	def send(self, msg, type="client", c=0, stfu=0):
		res=0
		msg=str(msg)
		if type == "client":
			if not stfu:
				print(f"[SocketObj/Client] send('{msg}')")
			res=self.obj.send(msg.encode())
		if type == "server":
			if not stfu:
				print(f"[SocketObj/Server] send('{msg}')")
			res=c.send(msg.encode())
		return res
	
	def accept(self, stfu=0):
		if not stfu:
			print(f"[SocketObj/Server] accept()")
		res = self.obj.accept()
		return res
	
	def getcode(self):
		sockn = self.obj.getsockname()
		code = f"{sockn[0].replace('.','&')}?{sockn[1]}"
		return code

class Server(SocketObj):
	def __init__(self, ip_port, slist=["SolEngine-Server","A Sol Server", 0]):
		SocketObj.__init__(self)
		SocketObj.make(self)
		SocketObj.bind(self, ip_port)
		SocketObj.listen(self)
		SocketObj.getcode(self)
		self.on = 1
		self.handle()
		self.data = {
			"player": {},
			"entity": {},
			"slvl": "slvl\x01\xFA\x02\x01\xFB\x02\x01\xFC\x02\xFF"
		}
		self.slist = slist
	
	def _handle(self):
		first=1
		while (self.on):
			c, addr = SocketObj.accept(self)
			
			t=threading.Thread(target=self._h1, args=(c,addr))
			t.start()
	
	def _h1(self,c,a):
		connected=1
		at=f"{a[0]}:{a[1]}"
		while connected:
			try:
				msg = c.recv(100).decode()
			except:
				msg="/??"
			
			if msg == "/join":
				print(f"[SocketObj/Server] Player {at} joined")
				self.slist[2] += 1
			elif msg == "/endserv":
				c.close()
				connected = 0
				self.on = 0
			elif msg == "/data":
				SocketObj.send(self, self.data, "server", c)
			elif msg == "/slist-data":
				SocketObj.send(self, self.slist, "server", c)
			elif msg == "/leave":
				print(f"[SocketObj/Server] Player {at} left")
				self.slist[2] -= 1
				c.close()
				connected=0
			elif msg == "/close":
				c.close()
				connected=0
		
	def handle(self):
		t=threading.Thread(target=self._handle)
		t.start()

class Client(SocketObj):
	def __init__(self, ip_port):
		SocketObj.__init__(self)
		SocketObj.make(self)
		SocketObj.connect(self, ip_port)
	
	def recv(self, bit=1024, send=None):
		time.sleep(0.01)
		res = SocketObj.recv(self, bit)
		if send:
			SocketObj.send(self, send)
		return res
	
	def send(self, msg):
		res = SocketObj.send(self, msg)
		return res

class ServerList(SocketObj):
	def __init__(self, ip, debug=0):
		SocketObj.make(self)
		self.out = SocketObj.listall(self, ip, debug=debug)

if __name__ == "__main__":
	ip=("", 1000)
	data = 0
	
	serv=Server(ip)
	ip=serv.ip
	
	client = Client(ip)
	client.send("/slist-data")
	data = client.recv(send="/leave")
	
	sl = ServerList(ip[0])
	print(sl.out)