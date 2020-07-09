import inky
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGrotesk
from math import sin
from random import uniform, random
import sqlite3
from pathlib import Path
import os
import geocoder
import requests
from bs4 import BeautifulSoup

class Weather():
	def __init__(self, address):
		coords = Weather.get_coords(address)
		print(coords)
		weather = {}
		res = requests.get("https://darksky.net/forecast/{}/uk212/en".format(",".join([str(c) for c in coords])))
		if res.status_code == 200:
			soup = BeautifulSoup(res.content, "lxml")
			curr = soup.find_all("span", "currently")
			self.weather = curr[0].img["alt"].split()[0]
			self.temp = int(curr[0].find("span", "summary").text.split()[0][:-1])
			press = soup.find_all("div", "pressure")
			self.pressure = int(press[0].find("span", "num").text)
		else:
			self.weather = None
			self.temp = None
			self.pressure = None

	@staticmethod
	def get_coords(address):
		g = geocoder.arcgis(address)
		coords = g.latlng
		return coords

## This maps the weather summary from Dark Sky
## to the appropriate weather icons
#icon_map = {
#    "snow": ["snow", "sleet"],
#    "rain": ["rain"],
#    "cloud": ["fog", "cloudy", "partly-cloudy-day", "partly-cloudy-night"],
#    "sun": ["clear-day", "clear-night"],
#    "storm": [],
#    "wind": ["wind"]
#}

#    for icon in icon_map:
#        if summary in icon_map[icon]:
#            weather_icon = icon
#            break

class Pirrigotchi():
	def __init__(self):
		self.db = PirriDB()
		self._inkyphat = inky.InkyPHAT('black')
		self._img = Image.new('P', (self._inkyphat.HEIGHT, self._inkyphat.WIDTH))
		self._draw = ImageDraw.Draw(self._img)
		self.pollsensor()
		self.chartsensor('sensor1', 'airtemp')
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

	def pollsensor(self):
		w = Weather('Allston, MA')
		airtemp = w.temp
		soiltemp = 0
		soilhum = 0
		lum = 0
		self.logsensor('sensor1', airtemp=airtemp, soiltemp=soiltemp, soilhum=soilhum, lum=lum)

	def logsensor(self, sensor, airtemp=0, soiltemp=0, soilhum=0, lum=0):
		c = self.db.cursor()
		c.execute('INSERT INTO data (soiltemp, soilhum, lum, airtemp, sensor) VALUES (?, ?, ?, ?, ?)', 
				(soiltemp, soilhum, lum, airtemp, sensor))
		self.db.commit()
	
	def chartsensor(self, sensor, value):
		c = self.db.cursor()
		query = f'''SELECT MIN(timestamp), MAX(timestamp), MIN({value}), MAX({value}), AVG({value})
			FROM data
                        WHERE timestamp >= datetime('now', '-1 days')
			GROUP BY strftime('%s', timestamp) / (60 * 30)
			'''
		print(query)
		for row in c.execute(query):
			print(row)

class PirriDB():
	def __init__(self):
		self._db = sqlite3.connect(os.sep.join([str(Path.home()), '.pirrigotchi-data.sqlite']))
	
	def cursor(self):
		if self._db:
			return self._db.cursor()
		return None

	def commit(self):
		self._db.commit()


def __main__():
	p = Pirrigotchi()

if __name__ == "__main__":
	__main__()
