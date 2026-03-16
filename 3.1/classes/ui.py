import pygame as pg
import random, moderngl as mgl, numpy as np
from collections import OrderedDict

class SurfaceCache:
	def __init__(self, max_size=10):
		self.cache = OrderedDict()
		self.max_size = max_size
		self.button_data = {}

	def cache_surface(self, key, surf):
		if len(self.cache) >= self.max_size:
			# Remove the least recently used item
			self.cache.popitem(last=False)
		self.cache[key] = surf

	def get_cached_surface(self, key):
		if key in self.cache:
			# Move to the end (most recently used)
			self.cache.move_to_end(key)
			return self.cache[key]
		return None

pg.font.init()
class Interface:
	def __init__(self, display, sfx, clk, res, gpumode, ctx):
		self.display = display
		self.ctx = ctx
		self.font = pg.font.Font(None, 35)
		self.sfx = sfx #SfxPlayer
		self.cache = SurfaceCache(max_size=10)
		self.gpumode =gpumode
		self.button_data = {}
		self.layerold = {}
		self.surfdats={}
		self.ticks = 0
		self.vertex = """
#version 330 core
in vec2 in_position;
in vec2 in_texcoord;
out vec2 v_texcoord;
void main() {
	gl_Position = vec4(in_position, 0.0, 1.0);
	v_texcoord = in_texcoord;
}
"""
		self.frag = """
#version 330 core
uniform sampler2D Texture;
in vec2 v_texcoord;
out vec4 f_color;
void main() {
	f_color = texture(Texture, v_texcoord);
}"""
		self.clk = clk #ClickSound
		self.iscl = {} #IsClicking
		self.IncludeDebugOverlays = 0
		self.frames = {}
		self.res = res
		self.cmpm = 0 #CompatibleMobileButtons
		self.inputs = {}
		self.INPUT_ETERNAL = {}
		self.dirty_rects = []
		self.layers = {}
		self.sliders = {}
		self.prog=0
		if self.gpumode:
			self.prog = self.ctx.program(vertex_shader = self.vertex, fragment_shader=self.frag)
			self.prog["Texture"].value = 0

	def input(self, size, pos, AlwaysOn=0, anchor="", scale=1, color="white", alpha=1, layer=0, special_flags=0, cache=False, rotation=0, disp="display", clip=0, flip=0, placeholder="", id=None, value="", event=None, frys=0):
		if event == None:
			event = pg.event.get()
		
		if disp == "display":
			disp = self.display
		
		if id == None:
			cache_key = f"InputObject-{size[0]}:{size[1]}:{scale}:{alpha}:{placeholder}:{rotation}:{size}:{flip}"
		else:
			cache_key = id
		
		if not cache_key in self.inputs:
			self.inputs[cache_key] = {
				"placeholder": placeholder,
				"value": value,
				"return": 0,
				"blink": 0,
				"selected": 0,
				"CAPS": 0
			}
		if not cache_key in self.INPUT_ETERNAL:
			self.INPUT_ETERNAL[cache_key] = {
				"placeholder": placeholder,
				"value": value,
				"return": 0,
				"blink": 0,
				"selected": 0,
				"CAPS": 0,
				"history": []
			}
		
		# Blink
		blnk="_"
		if self.inputs[cache_key]["blink"]:
			blnk="_"
		else:
			blnk="  "
		if not self.inputs[cache_key]["selected"] or not AlwaysOn:
			blnk="  "
		self.inputs[cache_key]["blink"] = not self.inputs[cache_key]["blink"]
		
		# Render input
		if self.inputs[cache_key]["value"] != "":
			f=self.res.render(self.inputs[cache_key]["value"]+blnk, color=color)
			surf = pg.Surface((f.get_width(), f.get_height()*2), pg.SRCALPHA)
			surf.blit(f, [10,10])
			
			if not AlwaysOn:
				inp = self.button(surf, pos, anchor, scale, alpha, 0, special_flags, cache, 0.1, disp, 0, frys=frys, layer=layer)
			else:
				inp = self.blit(surf, pos, anchor=anchor, scale=scale, alpha=alpha, disp=disp, layer=layer)
		else:
			f=self.res.render(self.inputs[cache_key]["placeholder"]+blnk, color=(127,127,127))
			surf = pg.Surface((f.get_width(), f.get_height()))
			surf.fill((200, 200, 200))
			surf.blit(f, [10,10])
			
			if not AlwaysOn:
				inp = self.button(surf, pos, anchor, scale, alpha, 0, special_flags, cache, 0.1, disp, 0, frys=frys, layer=layer)
			else:
				inp = self.blit(surf, pos, anchor=anchor, scale=scale, alpha=alpha, disp=disp, layer=layer)
		
		# Input logic
		if inp:
			self.inputs[cache_key]["selected"] = not self.inputs[cache_key]["selected"]
		
		if self.inputs[cache_key]["selected"] or AlwaysOn:
			for i in event:
				if i.type == pg.KEYDOWN:
					if i.key == pg.K_RETURN:
						try:
							hid=len(self.INPUT_ETERNAL[cache_key]["history"])-1
							if not (self.INPUT_ETERNAL[cache_key]["history"][hid] == self.inputs[cache_key]["value"]):
								self.INPUT_ETERNAL[cache_key]["history"].append(self.inputs[cache_key]["value"])
						except:
							self.INPUT_ETERNAL[cache_key]["history"].append(self.inputs[cache_key]["value"])
						self.inputs[cache_key]["return"] = 1
					elif i.key == pg.K_UP:
						hid=len(self.INPUT_ETERNAL[cache_key]["history"])-1
						self.inputs[cache_key]["value"] = self.INPUT_ETERNAL[cache_key]["history"][hid]
					elif i.key == pg.K_BACKSPACE:
						self.inputs[cache_key]["value"] = self.inputs[cache_key]["value"][:-1]
					elif i.key in [pg.K_CAPSLOCK, pg.K_LSHIFT, pg.K_RSHIFT]:
						self.inputs[cache_key]["CAPS"] = not self.inputs[cache_key]["CAPS"]
					else:
						try:
							val=chr(i.key)
						except:
							try:
								val=pg.key.name(i.key)
							except:
								val="?"
						if self.inputs[cache_key]["CAPS"]:
							val=val.upper()
						self.inputs[cache_key]["value"] += val
		
		return self.inputs[cache_key]["value"]
	
	def frame(self, size, pos, anchor="", sxs=1, scale=1, alpha=1, special_flags=0, cache=False, rotation=0, color=(200,200,200), disp="display", clip=0, flip=0, scrollable=1, id=None, frys=0, layer=0):
		surf = pg.Surface(size)
		surf.fill(color)
		dispd={}
		
		if disp=="display":
			disp=self.display
		else:
			if type(disp).__name__ == "dict":
				dispd=disp
				if "AvailabilityCheckIsDisplay" in dispd:
					disp=dispd["surf"]
				if "AvailabilityCheckIsFrameObject" in dispd and not frys:
					pos[0]-=self.frames[dispd["AvailabilityCheckIsFrameObject"]]["x"]
					pos[1]-=self.frames[dispd["AvailabilityCheckIsFrameObject"]]["y"]
			elif type(disp).__name__ == "Surface":
				disp=disp
		
		# Create a unique cache key
		if id == None:
			cache_key = f"Frame-{size[0]}:{size[1]}:{scale}:{alpha}:{24}:{rotation}:{size}:{flip}"
		else:
			cache_key = id
		
		if not cache_key in self.frames:
			self.frames[cache_key] = {"x": 0, "y": 0, "totaly": 0}
		data=self.frames[cache_key]
		
		if flip != 0:
			surf = pg.transform.flip(surf, flip)
		if rotation != 0:
			surf = pg.transform.rotate(surf, rotation)
		if scale != 1:
			surf = pg.transform.scale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
			if clip != 0:
				tmp=list(clip)
				clip=[
					tmp[0]*scale,
					tmp[1]*scale,
					tmp[2]*scale,
					tmp[3]*scale
				]
		if alpha != 1:
			surf.set_alpha(int(alpha * 255))

		# Adjust position based on anchor
		display_width = disp.get_width()
		display_height = disp.get_height()
		surf_width = surf.get_width()
		surf_height = surf.get_height()
		if clip:
			surf_width=clip[2]
			surf_height=clip[3]

		if "right" in anchor:
			pos[0] = display_width - pos[0] - surf_width
		if "bottom" in anchor:
			pos[1] = display_height - pos[1] - surf_height
		if "cx" in anchor:
			pos[0] += display_width / 2 - surf_width / 2
		if "cy" in anchor:
			pos[1] += display_height / 2 - surf_height / 2

		# blit the surface onto the display
		if clip:
			sprite = disp.blit(surf, pos, clip, special_flags=special_flags)
		else:
			sprite = disp.blit(surf, pos, special_flags=special_flags)

		# Check for mouse interactions
		get_mouse_rect = self.get_mouse_rect()

		# Check if hovering and calculate distance safely
		hovering = sprite.colliderect(get_mouse_rect)

		# Prevent division by zero in distance calculation
		x_dist = get_mouse_rect.x - sprite.x + 0.0001
		y_dist = get_mouse_rect.y - sprite.y + 0.0001

		distance = x_dist / y_dist
		click = pg.mouse.get_pressed()
		clicking_cmp = self.get_clicking(sprite, cache_key)
		if clip:
			sprite = self.blit(surf, pos, clip, special_flags=special_flags, layer=layer)
		else:
			sprite = self.blit(surf, pos, special_flags=special_flags, layer=layer)
		if scrollable:
			"""
			scroll_bar_is_big = max(1, (self.frames[cache_key]["y"] + 1) / 10)
			scroll_bar_size = max(20, 40 - (scroll_bar_is_big / 2))
			dys=data["y"]
			if dys > size[1] - 80 - (scroll_bar_is_big):
				dys=size[1] - 80 - (scroll_bar_is_big)
			barb = self.button(self.res.load(f"{self.res.resfol}/media/ui/scroll_y.png"), [25,25+dys], anchor="right", size=(20, 40 - (scroll_bar_size / 2)), scale=2-(sxs-1), disp=sprite, layer=layer)
			if barb:
				aftm = self.frames[cache_key]["y"] + ((pg.mouse.get_rel()[1] * (sxs /2)) + (scroll_bar_is_big/2))
				if aftm > 0 and aftm < size[1] - 80 - (scroll_bar_is_big):
					self.frames[cache_key]["y"] = aftm
					self.frames[cache_key]["totaly"] = aftm
			"""
			scroll_bar_is_big = max(1, (self.frames[cache_key]["y"] + 1) / 10)
			scroll_bar_size = max(20, 40 - (scroll_bar_is_big / 2))

			dys = self.frames[cache_key]["y"]
			dys = max(0, min(dys, size[1] - 80 - scroll_bar_size))

			scroll_bar = self.button(self.res.load(f"{self.res.resfol}/media/ui/scroll_y.png"),
                   [25, 25 + dys], anchor="right", size=(20, scroll_bar_size),
                   scale=2 - (sxs - 1), disp=sprite, layer=layer)

			if scroll_bar:
				mouse_pos = pg.mouse.get_pos()
				relative_y = mouse_pos[1] - pos[1]
				aftm = (relative_y / size[1]) * (size[1] - 80 - scroll_bar_is_big)
				aftm = max(0, min(aftm, size[1] - 80 - scroll_bar_is_big))
				self.frames[cache_key]["y"] = aftm
				self.frames[cache_key]["totaly"] = aftm


			# Return relevant Frame() information
			dataframe = {
				"sprite": sprite,
				"click": {
					0: clicking_cmp and click[0],
					1: clicking_cmp and click[1],
					2: clicking_cmp and click[2],
					"*": 1 in click
				},
					"FrameObjData": self.frames[cache_key],
					"hovering": hovering,
					"distance": distance,
					"AvailabilityCheckIsDisplay": 1,
					"AvailabilityCheckIsFrameObject": cache_key,
					"surf": surf,
					"Pos": pos
			}
			return dataframe
	
	def get_clicking(self, obj):
		for i in pg.event.get():
			if i.type == pg.MOUSEBUTTONDOWN:
				print("Perhaps")
				return 0
			elif i.type == pg.MOUSEBUTTONUP:
				print("Might")
				print(pg.mouse.get_pressed())
				if self.get_mouse_rect().colliderect(obj):
					print("Ye")
					return 1
	
	def rect(self, col, size):
		# Create a rectangle with a color
		surf = pg.Surface(size)
		surf.fill(col)
		return surf
	
	def tick(self):
		# Tick
		self.ticks += 1
	
	def fill(self, color, disp="display",alpha=1, off=[0,0],size="disp", anchor="", layer=0):
		if disp=="display":
			disp=self.display
		# Fill the screen
		if size=="disp":
			size=(disp.get_width(), disp.get_height())
		try:
			self.blit(self.rect(color, size), off, disp=disp, alpha=alpha, anchor=anchor, layer=layer)
		except:
			print("RectCol Err")
			
	# Function to create or reuse a button
	def button(self, surf, pos, id="", anchor="", mb_release_only=0, more_info_return=0, add_bg=0, size=0, scale=1, alpha=1, click=0, special_flags=0, cache=True, delta=0.1, oppo=0, disp="display", disabled=0, frys=0, layer=0, cooldown=0.1):
		if disp=="display":
			disp=self.display
		# Create a unique cache key based on the button's characteristics
		if id == "":
			button_id = f"Button-{surf.get_width()}:{surf.get_height()}:{scale}:{alpha}:{20}"
		else:
			button_id = id
		
		if not button_id in self.button_data:
			# Create and store the button in the cache if it doesn't exist
			self.button_data[button_id] = [1, alpha, 0]
		
		data = self.button_data[button_id]
		
		# Add White Backdrop so the button doesn't turn pitch black
		surft = pg.Surface(surf.get_size())
		surft.fill((255,255,255))

		if size == 0:
			size = surf.get_size()

		# blit the button and check if the button is being hovered
		if disabled:
			asset={"click": {}}
			asset_txtr = self.blit(surf, pos, anchor, scale, alpha/2, special_flags, add_bg=add_bg, button_release_only=mb_release_only, disp=disp, clks=0, frys=frys, size=size, layer=layer)
			asset["click"][1]=0
			asset["click"][2]=0
			asset["click"][3]=0
			asset["click"][0]=0
			asset["hovering"]=0
		else:
			asset = self.blit(surft, pos, anchor, scale, 0, special_flags, disp=disp, add_bg=add_bg, clks=0, frys=frys, size=size, layer=layer)#, button_release_only=mb_release_only)
			asset_txtr = self.blit(surf, pos, anchor, scale, alpha/data[0], special_flags, add_bg=add_bg, disp=disp, frys=frys, size=size, layer=layer)#, button_release_only=mb_release_only)
		
		if type(delta).__name__ != "int":
			delta = 0.1
		if oppo:
			if asset["hovering"]:
				if data[0] > alpha:
					data[0] -= delta
			else:
				if data[0] < 2:
					data[0] += delta
		else:
			if asset["hovering"]:
				if data[0] < 2:
					data[0] += delta
			else:
				if data[0] > alpha:
					data[0] -= delta
		
		clicked=asset["click"][click]
		if more_info_return:
			return asset
		return clicked
	
	#get_mouse_rect: Mouse rect
	def get_mouse_rect(self, width=10, height=10):
		# Get the current mouse position
		mouse_pos = pg.mouse.get_pos()

		# Create a pg.Rect based on the mouse position and desired size
		get_mouse_rect = pg.Rect(
			mouse_pos[0] - width // 2,  # Center the rect horizontally
			mouse_pos[1] - height // 2,  # Center the rect vertically
			width,					   # Width of the mouse rectangle
			height					   # Height of the mouse rectangle
		)

		return get_mouse_rect
	
	def blit(self, surf, pos, anchor="", scale=1, alpha=1, special_flags=0, cache=False, rotation=0,size=1, disp="display", clip=0, flip=0, clks=1, frys=0, sp=0, layer=0, id=0, add_bg=1, button_release_only=0):
		dispd={}
		if disp=="display":
			disp=self.display
		else:
			if type(disp).__name__ == "dict":
				dispd=disp
				if "AvailabilityCheckIsDisplay" in dispd:
					disp=dispd["surf"]
			elif type(disp).__name__ == "Surface":
				disp=disp
		if scale < 1:
			scale=1
		# Create a unique cache key
		try:
			cache_key = f"Surface-{surf.get_width()}:{surf.get_height()}:{scale}:{alpha}:{21}:{rotation}:{size}:{flip}"
		except:
			cache_key = f"Surface-Unknown-Unknown-{scale}-{alpha}-{rotation}-{size}-{flip}"
		
		if id == 0:
			id = len(self.layers)+1
		lk=f"{cache_key};{id}"
		if not lk in self.layers:
			self.layers[lk]={"data": {}}
		
		if cache:
			# Get from cache if available
			cached_surf = self.cache.get_cached_surface(cache_key)
			if cached_surf:
				surf = cached_surf
			else:
				# Apply transformations and cache it
				if size != 1:
					size=list(size)
					if size[0] < 1:
						size[0]=abs(size[0])
						pos[0]+=size[0]
					if size[1] < 1:
						size[1]=abs(size[1])
						pos[1]+=size[1]
					surf = pg.transform.scale(surf, size)
				if flip != 0:
					surf = pg.transform.flip(surf, flip[0], flip[1])
				if rotation != 0:
					surf = pg.transform.rotate(surf, rotation)
				if scale != 1:
					surf = pg.transform.scale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
					tmp=clip
					clip=[tmp[0]*scale, tmp[1]*scale, tmp[2]*scale, tmp[3]*scale]
				if alpha != 1:
					surf.set_alpha(int(alpha * 255))
				self.cache.cache_surface(cache_key, surf)
		else:
			# Apply transformations if not using cache
			if size != 1:
				size=list(size)
				if size[0] < 1:
					size[0]=abs(size[0])
					pos[0]-=size[0]
				if size[1] < 1:
					size[1]=abs(size[1])
					pos[1]-=size[1]
				surf = pg.transform.scale(surf, size)
			if flip != 0:
				surf = pg.transform.flip(surf, flip[0], flip[1])
			if rotation != 0:
				surf = pg.transform.rotate(surf, rotation)
			if scale != 1:
				surf = pg.transform.scale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
				if clip != 0:
					tmp=list(clip)
					clip=[
						tmp[0]*scale,
						tmp[1]*scale,
						tmp[2]*scale,
						tmp[3]*scale
					]
			if alpha != 1:
				surf.set_alpha(int(alpha * 255))

		# Default fallback surface if not valid
		if not surf:
			surf = pg.Surface((200, 200))
			surf.fill((255, 0, 0))

		# Adjust position based on anchor
		try:
			display_width = disp.get_width()
			display_height = disp.get_height()
		except:
			display_width = self.display.get_width()
			display_height = self.display.get_height()
		surf_width = surf.get_width()
		surf_height = surf.get_height()
		if clip:
			surf_width=clip[2]
			surf_height=clip[3]

		try:
			pos_old=pos
			pos = list(pos_old)
			if "right" in anchor:
				pos[0] = display_width - pos[0] - surf_width
			if "bottom" in anchor:
				pos[1] = display_height - pos[1] - surf_height
			if "cx" in anchor:
				pos[0] += display_width / 2 - surf_width / 2
			if "cy" in anchor:
				pos[1] += display_height / 2 - surf_height / 2
		except Exception as e:
			print(f"Anchors Broken {e}")
		if "AvailabilityCheckIsFrameObject" in dispd and not frys:
			pos[0]-=self.frames[dispd["AvailabilityCheckIsFrameObject"]]["x"]
			pos[1]-=self.frames[dispd["AvailabilityCheckIsFrameObject"]]["y"]

		sxo,syo=0,0
		if "AvailabilityCheckIsFrameObject" in dispd and not frys:
			sxo,syo=self.frames[dispd["AvailabilityCheckIsFrameObject"]]["x"], self.frames[dispd["AvailabilityCheckIsFrameObject"]]["y"]
		try:
			sprite=pg.rect.Rect((dispd["Pos"][0]+pos[0]-sxo, dispd["Pos"][1]+pos[1]-syo), (surf.get_width(), surf.get_height()))
		except:
			sprite=pg.rect.Rect((pos[0]-sxo, pos[1]-syo), (surf.get_width(), surf.get_height()))
		
		# Check for mouse interactions
		get_mouse_rect = self.get_mouse_rect()

		# Check if hovering and calculate distance safely
		if button_release_only:
			hovering=0
			for i in pg.event.get():
				if i.type == pg.MOUSEBUTTONUP:
					hovering=sprite.colliderect(get_mouse_rect)
		else:
			hovering = sprite.colliderect(get_mouse_rect)

		# Prevent division by zero in distance calculation
		x_dist = get_mouse_rect.x - sprite.x + 0.0001
		y_dist = get_mouse_rect.y - sprite.y + 0.0001

		distance = x_dist / y_dist
		click = pg.mouse.get_pressed()
		
		if "AvailabilityCheckIsDisplay" in dispd:
			self.blit(disp, dispd["Pos"])
		
		# Return relevant information
		data={
			"sprite": sprite,
			"click": {
				0: hovering and click[0],
				1: hovering and click[1],
				2: hovering and click[2],
				"*": 1 in click and hovering
			},
			"hovering": hovering,
			"distance": distance,
			"DNR":add_bg,
			"AvailabilityCheckIsDisplay": 1,
			"surf": surf,
			"Pos": pos,
			"Layer": layer,
			"LayerID": lk,
			"Clip": clip,
			"Disp": disp,
			"SetBlack": add_bg,
			"SpecialFlags": special_flags
		}
		self.layers[lk]["data"] = data
		if sp:
			print(sp, pos)
		self.dirty_rects.append(sprite)
		return data
	
	def render(self, fun=0, alpha=1, enginealphasupport=1):
		if 0:
			self.blit(self.font.render(f"RenderedObj: {len(self.layers)}", 0, "white"), [0,0], layer=200)
		
		objects={}
		
		layersorg = {}
		for i, (key, e) in enumerate(sorted(self.layers.items(), key=lambda x: x[1]["data"].get("Layer", 0))):
			layersorg[i + 1] = e
		
		
		if self.gpumode:
			self.ctx.clear(0.1,0.1,0.1)
			self.ctx.enable(mgl.BLEND)
			self.ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA)
		for i in layersorg:
			layerdata=layersorg[i]["data"]

			disp,surf,pos,clip,special_flags,sb=layerdata["Disp"],layerdata["surf"],layerdata["Pos"],layerdata["Clip"],layerdata["SpecialFlags"],layerdata["SetBlack"]

			if sb:
				surfold=surf
				surf=pg.Surface(surfold.get_size())
				surf.fill("black")
				surf.blit(surfold,[0,0])
			if alpha != 1:
				surf.set_alpha(alpha)
			
			if fun:
				sizec=random.randint(1,surf.get_width()),random.randint(1,surf.get_height())
				posc=random.randint(0,(surf.get_width()-sizec[0])),random.randint(0,(surf.get_height()-sizec[1]))
				clip=(posc,sizec)
			
			if not enginealphasupport:
				surf=surf.convert()
			if self.gpumode:
				if clip:
					spritegpu = pg.Surface((clip[2],clip[3]))
					spritegpu.blit(surf, [0,0], clip, special_flags=special_flags)
				else:
					spritegpu = pg.Surface(surf.get_size())
					spritegpu.blit(surf, [0,0], special_flags=special_flags)
				surfdat = pg.image.tostring(surf, "RGBA", True)
				if not surfdat in self.surfdats:
					w,h=surf.get_size()
					txt=self.ctx.texture((w,h),4,data=surfdat,alignment=1)
					txt.filter = (mgl.NEAREST, mgl.NEAREST)
					self.surfdats[surfdat] = txt
				else:
					txt=self.surfdats[surfdat]	
				txt.use(location=0)
				left=(pos[0] / self.display.get_width()) * 2 - 1
				right=((pos[0] + surf.get_width()) / self.display.get_width()) * 2 - 1
				top = 1 - (pos[1] / self.display.get_height()) * 2
				bottom = 1 - ((pos[1] + surf.get_height()) / self.display.get_height()) * 2
				
				prog,vertices,vbo,vao=self.make_gpu_stuff(left,right,bottom,top)
				txt.use()
				vao.render(mgl.TRIANGLE_FAN)
			else:
				try:
					if clip:
						sprite = disp.blit(surf, pos, clip, special_flags=special_flags)
					else:
						sprite = disp.blit(surf, pos, special_flags=special_flags)
				except:
					if clip:
						sprite = self.display.blit(surf, pos, clip, special_flags=special_flags)
					else:
						sprite = self.display.blit(surf, pos, special_flags=special_flags)
		self.layerold=self.layers
		self.layers={}
	def make_gpu_stuff(self, left,right,bottom,top):
		vertices = np.array([
			left, bottom, 0.0, 0.0,
			right, bottom, 1.0, 0.0,
			right, top, 1.0, 1.0,
			left, top, 0.0, 1.0,
		], dtype="f4")
		
		vbo = self.ctx.buffer(vertices.tobytes())
		vao = self.ctx.simple_vertex_array(self.prog, vbo, "in_position", "in_texcoord")
		return self.prog,vertices,vbo,vao
	
	def slider(self, x, y, min_value=0, max_value=100, initial_value=50, out_type=["int", 0], disp="display", width=200, id=0, layer=2):
		if id == 0:
			id = f"Slider-D{initial_value};M{min_value};MX{max_value};S{width};P{x},{y}"
		if id not in self.sliders:
			self.sliders[id] = [initial_value, 0, initial_value]
		value = self.sliders[id][0]

		# Slider state
		rect = pg.Rect(x, y, width, 20)  # Slider bar
		knob_rect = pg.Rect(0, 0, 20, 20)  # Knob rectangle
		dragging = self.sliders[id][1]

		# Handle String Mode: Calculate step width and snap knob to string positions
		if out_type[0] == "str":
			options = out_type[1]
			num_steps = len(options)
			step_width = rect.width / (num_steps - 1) if num_steps > 1 else rect.width

			# If the slider value is a string, find its position index
			if isinstance(self.sliders[id][0], str):
				try:
					current_index = options.index(self.sliders[id][0])
				except ValueError:
					current_index = 0
			else:
				current_index = 0
			knob_rect.centerx = rect.left + current_index * step_width
		else:
			# Numeric mode
			knob_rect.centerx = rect.left + ((self.sliders[id][0] - min_value) / (max_value - min_value)) * rect.width
		knob_rect.centery = rect.centery

		# If dragging, update knob position and value
		if dragging:
			mouse_x = self.get_mouse_rect().x
			self.sliders[id][2] = mouse_x
			knob_rect.centerx = max(rect.left, min(mouse_x, rect.right))  # Clamp knob within slider

			if out_type[0] == "str":
				# Snap to nearest string option
				current_index = round((knob_rect.centerx - rect.left) / step_width)
				current_index = max(0, min(current_index, num_steps - 1))  # Clamp to valid range
				self.sliders[id][0] = options[current_index]
				knob_rect.centerx = rect.left + current_index * step_width
			else:
				# Numeric modes
				self.sliders[id][0] = min_value + ((knob_rect.centerx - rect.left) / rect.width) * (max_value - min_value)
				if out_type[0] == "int":
					self.sliders[id][0] = round(self.sliders[id][0])
				elif out_type[0] == "float":
					self.sliders[id][0] = float(self.sliders[id][0])

		# Draw the slider bar
		bar_surface = pg.Surface((width + 24, 24), pg.SRCALPHA)
		bar_surface.fill((42, 42, 52))
		pg.draw.rect(bar_surface, (66, 66, 85), (0, 0, width + 24, 24), 2)
		textvar=self.blit(self.res.render(self.sliders[id][0], size=25), [0, 0], anchor="cx cy", add_bg=0, disp=bar_surface)

		# Knob surfaces for normal, hover, and active states
		knob_surface = pg.Surface((20, 20), pg.SRCALPHA)
		knob_surface.fill((66, 150, 250))
		knob_hover = pg.Surface((20, 20), pg.SRCALPHA)
		knob_hover.fill((76, 170, 255))
		knob_active = pg.Surface((20, 20), pg.SRCALPHA)
		knob_active.fill((90, 180, 250))

		# Blit the slider bar and knob
		y -= 2
		x -= 12
		self.blit(bar_surface, (x, y), disp=disp, layer=layer)
		self.blit(self.res.render(self.sliders[id][0], size=25), textvar["Pos"], add_bg=0, disp=disp, layer=layer+2)
		knob_obj = self.blit(knob_surface, knob_rect.topleft, disp=disp, layer=layer + 1)

		# Update dragging and hovering states
		self.sliders[id][1] = knob_obj["click"][0]
		if knob_obj["click"][0]:
			self.blit(knob_active, knob_rect.topleft, disp=disp, layer=layer + 1)
		if knob_obj["hovering"]:
			self.blit(knob_hover, knob_rect.topleft, disp=disp, layer=layer + 1)

		# Draw labels for string mode
		if out_type[0] == "str":
			font = pg.font.Font(None, 20)  # Default font
			for i, option in enumerate(options):
				label_surface = font.render(option, True, (255, 255, 255))
				label_x = rect.left + i * step_width - label_surface.get_width() // 2
				label_y = rect.bottom + 5
				self.blit(label_surface, (label_x, label_y), disp=disp, layer=layer)

		return value