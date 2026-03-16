import pygame as pg
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

class Interface:
	def __init__(self, display, sfx, clk, res):
		self.display = display
		self.sfx = sfx #SfxPlayer
		self.cache = SurfaceCache(max_size=10)
		self.button_data = {}
		self.ticks = 0
		self.clk = clk #ClickSound
		self.iscl = {} #IsClicking
		self.frames = {}
		self.res = res
		self.cmpm = 0 #CompatibleMobileButtons
		self.inputs = {}
		self.sliders = {}
	
	def input(self, size, pos, anchor="", scale=1, alpha=1, special_flags=0, cache=False, rotation=0, disp="display", clip=0, flip=0, placeholder="", id=None, value="", event=None, frys=0):
		if event == None:
			event = pg.event.get()
		
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
				"selected": 0
			}
		
		# Blink
		blnk="_"
		if self.inputs[cache_key]["blink"]:
			blnk="_"
		else:
			blnk=" "
		if not self.inputs[cache_key]["selected"]:
			blnk=" "
		self.inputs[cache_key]["blink"] = not self.inputs[cache_key]["blink"]
		
		# Render input
		if self.inputs[cache_key]["value"] != "":
			surf = pg.Surface(size)
			surf.fill((200, 200, 200))
			surf.blit(self.res.render(self.inputs[cache_key]["value"]+blnk, color="black"), [10,10])
			
			inp = self.button(surf, pos, anchor, scale, alpha, 0, special_flags, cache, 0.1, disp, 0, frys=frys)
		else:
			surf = pg.Surface(size)
			surf.fill((200, 200, 200))
			surf.blit(self.res.render(self.inputs[cache_key]["placeholder"]+blnk, color=(127,127,127)), [10,10])
			
			inp = self.button(surf, pos, anchor, scale, alpha, 0, special_flags, cache, 0.1, disp, 0, frys=frys)
		
		# Input logic
		if inp:
			self.inputs[cache_key]["selected"] = not self.inputs[cache_key]["selected"]
		
		if self.inputs[cache_key]["selected"]:
			for i in event:
				if i.type == pg.KEYDOWN:
					if i.key == pg.K_RETURN:
						self.inputs[cache_key]["return"] = 1
					elif i.key == pg.K_BACKSPACE:
						self.inputs[cache_key]["value"] = self.inputs[cache_key]["value"][:-1]
					else:
						try:
							self.inputs[cache_key]["value"] += chr(i.key)
						except:
							try:
								self.inputs[cache_key]["value"] += pg.key.name(i.key)
							except:
								pass
		
		return self.inputs[cache_key]["value"]
	
	def frame(self, size, pos, anchor="", sxs=1, scale=1, alpha=1, special_flags=0, cache=False, rotation=0, disp="display", clip=0, flip=0, scrollable=1, id=None, frys=0):
		surf = pg.Surface(size)
		surf.fill((200, 200, 200))
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
			self.frames[cache_key] = {"x": 0, "y": 0}
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

		# Blit the surface onto the display
		if clip:
			sprite = disp.blit(surf, pos, clip, special_flags=special_flags)
		else:
			sprite = disp.blit(surf, pos, special_flags=special_flags)

		# Check for mouse interactions
		mrect = self.mrect()

		# Check if hovering and calculate distance safely
		hovering = sprite.colliderect(mrect)

		# Prevent division by zero in distance calculation
		x_dist = mrect.x - sprite.x + 0.0001
		y_dist = mrect.y - sprite.y + 0.0001

		distance = x_dist / y_dist
		click = pg.mouse.get_pressed()
		clicking_cmp = self.clicking(sprite, cache_key)
		if clip:
			sprite = self.blit(surf, pos, clip, special_flags=special_flags)
		else:
			sprite = self.blit(surf, pos, special_flags=special_flags)
		if scrollable:
			barb = self.button(self.res.load(f"{self.res.resfol}/media/ui/scroll_y.png"), [25,25+(data["y"])], anchor="right", scale=2-(sxs-1), disp=sprite)
			if barb:
				aftm = self.frames[cache_key]["y"] + (pg.mouse.get_rel()[1] * sxs)
				if aftm > 0 and aftm < size[1]-125:
					self.frames[cache_key]["y"] = aftm

		# Return relevant Frame() information
		return {
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
	
	def clicking(self, obj, id=1):
		if not id in self.iscl:
			self.iscl[id] = 0
		if self.cmpm:
			for i in pg.event.get():
				if i.type == pg.MOUSEBUTTONDOWN:
					if obj.colliderect(self.mrect()):
						self.iscl[id] = 1
				elif i.type == pg.MOUSEBUTTONUP:
					self.iscl[id] = 0
		else:
			self.iscl[id] = obj.colliderect(self.mrect())
		return self.iscl[id]

	def rect(self, col, size):
		# Create a rectangle with a color
		surf = pg.Surface(size)
		surf.fill(col)
		return surf
	
	def tick(self):
		# Tick
		self.ticks += 1
	
	def fill(self, color, disp="display",alpha=1):
		if disp=="display":
			disp=self.display
		# Fill the screen
		self.blit(self.rect(color, (disp.get_width(), disp.get_height())), [0,0], disp=disp, alpha=alpha)
	
	# Function to create or reuse a button
	def button(self, surf, pos, anchor="", scale=1, alpha=1, click=0, special_flags=0, cache=True, delta=0.1, disp="display", disabled=0, frys=0):
		if disp=="display":
			disp=self.display
		# Create a unique cache key based on the button's characteristics
		button_id = f"Button-{surf.get_width()}:{surf.get_height()}:{scale}:{alpha}:{20}"
		
		if not button_id in self.button_data:
			# Create and store the button in the cache if it doesn't exist
			self.button_data[button_id] = [1, alpha]
		
		data = self.button_data[button_id]
		
		# Add White Backdrop so the button doesn't turn pitch black
		surft = pg.Surface(surf.get_size())
		surft.fill((255,255,255))
		
		# Draw the button and check if the button is being hovered
		if disabled:
			asset={"click": {}}
			asset_txtr = self.blit(surf, pos, anchor, scale, alpha/2, special_flags, disp=disp, clks=0, frys=frys)
			asset["click"][1]=0
			asset["click"][2]=0
			asset["click"][3]=0
			asset["click"][0]=0
			asset["hovering"]=0
		else:
			asset = self.blit(surft, pos, anchor, scale, 0, special_flags, disp=disp, clks=0, frys=frys)
			asset_txtr = self.blit(surf, pos, "", scale, alpha/data[0], special_flags, disp=disp, frys=frys)
		
		if asset["hovering"]:
			if data[0] < 2:
				data[0] += delta
		else:
			if data[0] > alpha:
				data[0] -= delta
		
		return asset["click"][click]
	
	#mrect: Mouse rect
	def mrect(self, width=10, height=10):
		# Get the current mouse position
		mouse_pos = pg.mouse.get_pos()

		# Create a pg.Rect based on the mouse position and desired size
		mrect = pg.Rect(
			mouse_pos[0] - width // 2,  # Center the rect horizontally
			mouse_pos[1] - height // 2,  # Center the rect vertically
			width,					   # Width of the mouse rectangle
			height					   # Height of the mouse rectangle
		)

		return mrect
	
	def blit(self, surf, pos, anchor="", scale=1, alpha=1, special_flags=0, cache=False, rotation=0,size=1, disp="display", clip=0, flip=0, clks=1, frys=0):
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
		# Create a unique cache key
		cache_key = f"Surface-{surf.get_width()}:{surf.get_height()}:{scale}:{alpha}:{21}:{rotation}:{size}:{flip}"

		if cache:
			# Get from cache if available
			cached_surf = self.cache.get_cached_surface(cache_key)
			if cached_surf:
				surf = cached_surf
			else:
				# Apply transformations and cache it
				if size != 1:
					surf = pg.transform.scale(surf, size)
				if flip != 0:
					surf = pg.transform.flip(surf, flip)
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
				surf = pg.transform.scale(surf, size)
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

		# Default fallback surface if not valid
		if not surf:
			surf = pg.Surface((200, 200))
			surf.fill((255, 0, 0))

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
		
		if "AvailabilityCheckIsFrameObject" in dispd and not frys:
			pos[0]-=self.frames[dispd["AvailabilityCheckIsFrameObject"]]["x"]
			pos[1]-=self.frames[dispd["AvailabilityCheckIsFrameObject"]]["y"]
		
		# Blit the surface onto the display
		if clip:
			sprite = disp.blit(surf, pos, clip, special_flags=special_flags)
		else:
			sprite = disp.blit(surf, pos, special_flags=special_flags)

		# Check for mouse interactions
		mrect = self.mrect()

		# Check if hovering and calculate distance safely
		hovering = sprite.colliderect(mrect)

		# Prevent division by zero in distance calculation
		x_dist = mrect.x - sprite.x + 0.0001
		y_dist = mrect.y - sprite.y + 0.0001

		distance = x_dist / y_dist
		click = pg.mouse.get_pressed()
		sxo,syo=0,0
		if "AvailabilityCheckIsFrameObject" in dispd and not frys:
			sxo,syo=self.frames[dispd["AvailabilityCheckIsFrameObject"]]["x"], self.frames[dispd["AvailabilityCheckIsFrameObject"]]["y"]
		try:
			spritehb=pg.rect.Rect((dispd["Pos"][0]+pos[0]-sxo, dispd["Pos"][1]+pos[1]-syo), (surf.get_width(), surf.get_height()))
		except:
			spritehb=sprite
		
		clicking_cmp = self.clicking(spritehb, cache_key)
		
		if clicking_cmp and 1 in click and clks:
			self.sfx.play(self.clk, cc="click.mp3")
		
		if "AvailabilityCheckIsDisplay" in dispd:
			self.blit(disp, dispd["Pos"])
		
		# Return relevant information
		return {
			"sprite": sprite,
			"click": {
				0: clicking_cmp and click[0],
				1: clicking_cmp and click[1],
				2: clicking_cmp and click[2],
				"*": 1 in click
			},
			"hovering": hovering,
			"distance": distance,
			"AvailabilityCheckIsDisplay": 1,
			"surf": surf,
			"Pos": pos
		}
	
	def slider(self, pos, value=1, min=0, max=1, anchor="", scale=1, disp="display", id=0):
		if id == 0:
			id = f"Slider-D{value};M{min};MX{max};S{scale};P{pos}"
		if not id in self.sliders:
			self.sliders[id] = value
		val = self.sliders[id]
			
		ca=(max-min)
		sbpos=[pos[0], pos[1]+(20)]
		spos=[val, 0]
		#sdtpos=[ca+20, pos[1]+10]
		
		sd=pg.Surface((30,50))
		sd.fill((0,0,0))
		
		sbd=pg.Surface((ca,10))
		sbd.fill((127,127,127))
		
		settingb=self.blit(sbd, sbpos, anchor=anchor, disp=disp)
		setting=self.blit(sd, [settingb["sprite"].x + spos[0], settingb["sprite"].y],anchor="",disp="display")
		#stdat=self.button(self.res.render(f"{val}", color="black"), sdtpos, disp=settingb)
		
		return [setting["click"][0], self.sliders[id]]