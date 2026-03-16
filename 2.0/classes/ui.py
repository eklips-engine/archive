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
	def __init__(self, display, sfx, clk):
		self.display = display
		self.sfx = sfx
		self.cache = SurfaceCache(max_size=10)
		self.button_data = {}
		self.ticks = 0
		self.clk = clk

	def rect(self, col, size):
		# Create a rectangle with a color
		surf = pg.Surface(size)
		surf.fill(col)
		return surf
	
	def tick(self):
		# Tick
		self.ticks += 1
	
	def shader(self, name):
		# Shaders!
		if name == "crash":
			dw2 = self.display.get_width() / 2
			dh2 = self.display.get_height() / 2
			
			self.blit(self.hue(self.display, 240), [-dw2, -dh2])
			self.blit(self.hue(self.display, 120), [dw2, dh2])
			self.display.surface = self.hue(self.display.surface)
	
	def hue(self, surface, shift, cache=0):
		# Self-explanatory, It changes the hue
		cache_key = f"HueSurf-{surface.get_width()}:{surface.get_height()}:{shift}:{220}"

		if cache:
			# Get from cache if available
			cached_surf = self.cache.get_cached_surface(cache_key)
			if cached_surf:
				surface = cached_surf
			else:
				pixels = pg.PixelArray(surface)
				# Iterate over every pixel
				for x in range(surface.get_width()):
					for y in range(surface.get_height()):
						# Turn the pixel data into an RGB tuple
						rgb = surface.unmap_rgb(pixels[x][y])
						# Get a new color object using the RGB tuple and convert to HSLA
						color = Color(*rgb)
						h, s, l, a = color.hsla
						# Shift the hue
						color.hsla = (int(h) + shift) % 360, int(s), int(l), int(a)
						# Assign directly to the pixel
						pixels[x][y] = color
				
				# Turn it into a Surface
				surface = pg.surfarray.make_surface(pixels)
				
				# Cache it
				if cache:
					self.cache.cache_surface(cache_key, surface)
				
				# The old way of closing a PixelArray object
				del pixels
		return surface
	
	def fill(self, color):
		# Fill the screen
		pg.draw.rect(self.display, color, (0,0, self.display.get_width(), self.display.get_height()))
	
	# Function to create or reuse a button
	def button(self, surf, pos, anchor="", scale=1, alpha=1, click=0, special_flags=0, cache=True, delta=0.1):
		# Create a unique cache key based on the button's characteristics
		button_id = f"Button-{surf.get_width()}:{surf.get_height()}:{scale}:{alpha}:{20}"
		
		if not button_id in self.button_data:
			# Create and store the button in the cache if it doesn't exist
			self.button_data[button_id] = [0, alpha]
		
		data = self.button_data[button_id]
		
		# Add White Backdrop so the button doesn't turn pitch black
		surft = pg.Surface(surf.get_size())
		surft.fill((255,255,255))
		
		# Draw the button and check if the button is being hovered
		asset 	   = self.blit(surft, pos, anchor, scale, data[1], special_flags)
		asset_txtr = self.blit(surf, pos, "", scale, alpha, special_flags)
		
		if asset["hovering"]:
			if data[0] > 0:
				data[0] -= delta
				data[1] += delta
		else:
			if data[0] < alpha:
				data[0] += delta
				data[1] -= delta
		dark_asset = self.blit(surf, pos, "", scale, data[0], special_flags=pg.BLEND_MULT)
		
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
	
	def blit(self, surf, pos, anchor="", scale=1, alpha=1, special_flags=0, cache=False, rotation=0):
		# Create a unique cache key
		cache_key = f"Surface-{surf.get_width()}:{surf.get_height()}:{scale}:{alpha}:{21}:{rotation}"

		if cache:
			# Get from cache if available
			cached_surf = self.cache.get_cached_surface(cache_key)
			if cached_surf:
				surf = cached_surf
			else:
				# Apply transformations and cache it
				if rotation != 0:
					surf = pg.transform.rotate(surf, rotation)
				if scale != 1:
					surf = pg.transform.scale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
				if alpha != 1:
					surf.set_alpha(int(alpha * 255))
				self.cache.cache_surface(cache_key, surf)
		else:
			# Apply transformations if not using cache
			if scale != 1:
				surf = pg.transform.scale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
			if rotation != 0:
				surf = pg.transform.rotate(surf, rotation)
			if alpha != 1:
				surf.set_alpha(int(alpha * 255))

		# Default fallback surface if not valid
		if not surf:
			surf = pg.Surface((200, 200))
			surf.fill((255, 0, 0))

		# Adjust position based on anchor
		display_width = self.display.get_width()
		display_height = self.display.get_height()

		if "right" in anchor:
			pos[0] = display_width - pos[0] - surf.get_width()
		if "bottom" in anchor:
			pos[1] = display_height - pos[1] - surf.get_height()
		if "cx" in anchor:
			pos[0] += display_width / 2 - surf.get_width() / 2
		if "cy" in anchor:
			pos[1] += display_height / 2 - surf.get_height() / 2

		# Blit the surface onto the display
		sprite = self.display.blit(surf, pos, special_flags=special_flags)

		# Check for mouse interactions
		mrect = self.mrect()

		# Check if hovering and calculate distance safely
		hovering = sprite.colliderect(mrect)

		# Prevent division by zero in distance calculation
		x_dist = mrect.x - sprite.x + 0.0001
		y_dist = mrect.y - sprite.y + 0.0001

		distance = x_dist / y_dist
		click = pg.mouse.get_pressed()
		for i in click:
			if i == 1 and hovering:
				self.sfx.play(self.clk)

		# Return relevant information
		return {
			"sprite": sprite,
			"click": {
				0: hovering and click[0],
				1: hovering and click[1],
				2: hovering and click[2]
			},
			"hovering": hovering,
			"distance": distance
		}