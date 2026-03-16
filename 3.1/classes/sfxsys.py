import pygame as pg
import random
import numpy as np
from scipy.signal import convolve

pg.init()

class SoundSystem:
	def __init__(self):
		self.cc=[]
		self.sfx = {}
		self.mcc=5
		self.dvol = 1
		self.ccf={}
		nl="\n"
		try:
			for i in open(f"{open('game.txt').read().split(nl)[1]}/media/sfx.txt"):
				di=i.split()
				self.ccf[di[0]] = " ".join(di[1:])
		except:
			pass
	def play(self, sfx, pos_to=[0,0], pos_at=[0,0],loop=0, volume="Default", cc="??"):
		id = f"Sound-{len(self.sfx)}-{loop}-{volume}-POS{pos_at},{pos_to}"
		
		if volume == "Default":
			volume = self.dvol
		
		if not (sfx or type(sfx).__name__ == "pygame.mixer.Sound"):
			sfx = self.generate_fallback_sound()
			volume = 1000
		
		try:
			sfx.set_volume(volume/100)
			sfx.play(loop)
			self.cc.append(cc)
			self.sfx[id] = [sfx, pos_to, loop]
		except:
			print("Sound systen broken sounds (??)")
	
	def generate_fallback_sound(self, frequency=440, duration=1.0, sample_rate=44100, volume=1.0):
		noise=random.randint(0,1) #Phone call or water hose?
		if noise:
			num_samples = int(sample_rate * duration)
			# Generate random data between -1 and 1
			wave = np.random.uniform(-1, 1, num_samples) * volume
			wave = np.int16(wave * 32767)  # Convert to 16-bit PCM format
			sound_array = np.stack([wave, wave], axis=-1)  # Make it stereo
			sound = pg.sndarray.make_sound(sound_array)
		else:
			t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
			wave = 0.5 * volume * np.sin(2 * np.pi * frequency * t)
			wave = np.int16(wave * 32767)  # Convert to 16-bit PCM format
			sound_array = np.stack([wave, wave], axis=-1)  # Make it stereo
			sound = pg.sndarray.make_sound(sound_array)
		return sound
	
	def stop(self, id):
		if id in self.sfx:
			self.sfx[id][0].stop()
		else:
			print("Sound system no sound")
	
	def vol(self, id, volu):
		if id in self.sfx:
			self.sfx[id][0].set_volume(volu)
		else:
			print("Sound system no sound")
	
	def apply_echo(self, sound, delay=0.2, decay=0.5):
		raw = pg.sndarray.array(sound)
		delay_samples = int(delay * pg.mixer.get_init()[0])
		echo_filter = np.zeros(delay_samples)
		echo_filter[0] = 1
		echo_filter[-1] = decay
		echoed_sound = convolve(raw, echo_filter, mode='full')
		sound_with_echo = pg.sndarray.make_sound(echoed_sound.astype(np.int16))
		return sound_with_echo

	def apply_reverb(self, sound, decay=0.5):
		raw = pg.sndarray.array(sound)
		reverb_filter = np.random.uniform(-1, 1, raw.shape).astype(np.float32)
		reverb_filter *= decay / np.max(np.abs(reverb_filter))
		reverb_sound = raw + reverb_filter * np.roll(raw, 1, axis=0)
		sound_with_reverb = pg.sndarray.make_sound(reverb_sound.astype(np.int16))
		return sound_with_reverb
	
	def reverse(self, sound):
		try:
			raw = pg.sndarray.array(sound)
			reversed_sound = raw[::-1]
			sound_reversed = pg.sndarray.make_sound(reversed_sound)
			return sound_reversed
		except:
			print("Sound system broken soundRV")
		
	def sound_done(self):
		self.sfx={}