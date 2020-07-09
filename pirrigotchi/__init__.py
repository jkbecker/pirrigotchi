import inky
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGrotesk
from math import sin
from random import uniform, random


class Pirrigotchi():
	def __init__(self):
		self._inkyphat = inky.InkyPHAT('black')
		self._img = Image.new('P', (self._inkyphat.HEIGHT, self._inkyphat.WIDTH))
		self._draw = ImageDraw.Draw(self._img)
		font = ImageFont.truetype(HankenGrotesk, 14)
		message = "Hello, World!"
		h, w = font.getsize(message)
		x = (self._inkyphat.WIDTH / 2) - (w / 2)
		y = (self._inkyphat.HEIGHT / 2) - (h / 2)
		self._draw.text((y,x), message, self._inkyphat.BLACK, font)
		oldmin = 0
		oldmax = 0
		oldpoint = 0
		for i in range(48):
			point = 0.5*(oldpoint + sin(.1*i)+uniform(-.2,.2))
			min = 0.5*(oldmin + point-uniform(0,1))
			max = 0.5*(oldmax + point+uniform(0,1))
			scale=10
			self._draw.line((i, 40-scale*min, i, 40-scale*max), self._inkyphat.RED, 1)
			self._draw.point((i, 40-scale*point), self._inkyphat.BLACK)
			oldmin = min
			oldmax = max
			oldpoint = point
		self._inkyphat.set_image(self._img.rotate(90, Image.NEAREST, expand=1))
		self._inkyphat.set_border(self._inkyphat.BLACK)
		self._inkyphat.show()

def __main__():
	p = Pirrigotchi()

if __name__ == "__main__":
	__main__()
