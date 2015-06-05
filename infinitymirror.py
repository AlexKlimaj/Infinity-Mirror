# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import RPi.GPIO as GPIO
import time
from datetime import datetime
#from datetime import time
import thread
from neopixel import *
from threading import Thread
from astral import Astral
import random

############################################################################

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

############################################################################

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
BOUNCETIME = 300 #Button debounce time in ms
BUTTON_PRESSED = False

MODE = 0 #defines the mode to display. Mode 0 is the clock
NUMBEROFMODES = 8 #How many modes to cycle through

CITY_NAME = 'Denver'

############################################################################

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	global BUTTON_PRESSED
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		if BUTTON_PRESSED == True:
			return
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	global BUTTON_PRESSED
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
				if BUTTON_PRESSED == True:
					return
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	global BUTTON_PRESSED
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
			if BUTTON_PRESSED == True:
				return
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	global BUTTON_PRESSED
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
			if BUTTON_PRESSED == True:
				return
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	global BUTTON_PRESSED
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
				if BUTTON_PRESSED == True:
					return
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)
                
def clock(strip, city):
	"""Make the mirror into a clock"""
    #now = datetime.time(now.hour, now.minute, now.second)
	
	secondcolor = Color(25, 25, 25) #White
	minutecolor = Color(255, 0, 0) #Red
	off = Color(0, 0, 0) #off
	
	now = datetime.now()
	
	#print('%s' % str(datetime.now()))
	sun = city.sun(date=None, local=True)
	#print('Sunrise: %s' % str(sun['sunrise']))
	#print('Sunset:  %s' % str(sun['sunset']))
	
	hourcolor = Color(255,255,0) #Yellow
	#if datetime.utcnow() > city.sunrise(date=None, local=False) and datetime.utcnow() < city.sunset(date=None, local=False):
	#	hourcolor = Color(255,255,0) #Yellow
	#else:
	#	hourcolor = Color(106,90,205) #slateblue
	
	#print ("Current hour = %s" %now.hour)
	if now.second > 38:
		second = -now.second + 98
	else:
		second = -now.second + 38
	lasts = second + 1
	if second !=  1:
		strip.setPixelColor(0, off)
	
	strip.setPixelColor(lasts, off)
	
	
	if now.minute > 38:
		minute = -now.minute + 98
	else:
		minute = -now.minute + 38
	lastminute = minute + 1
	if lastminute > 60:
		lastminute = 1
	strip.setPixelColor(lastminute, off)
	
	
	if now.hour > 12:
		hour = now.hour - 12
	else:
		hour = now.hour
	
	if hour == 1:
		for x in xrange(36, 41):
			strip.setPixelColor(x, off)
		for x in xrange(31, 36):
			strip.setPixelColor(x, hourcolor)
	if hour == 2:
		for x in xrange(31, 36):
			strip.setPixelColor(x, off)
		for x in xrange(26, 31):
			strip.setPixelColor(x, hourcolor)
	if hour == 3:
		for x in xrange(26, 31):
			strip.setPixelColor(x, off)
		for x in xrange(21, 26):
			strip.setPixelColor(x, hourcolor)
	if hour == 4:
		for x in xrange(21, 26):
			strip.setPixelColor(x, off)
		for x in xrange(16, 21):
			strip.setPixelColor(x, hourcolor)
	if hour == 5:
		for x in xrange(16, 21):
			strip.setPixelColor(x, off)
		for x in xrange(11, 16):
			strip.setPixelColor(x, hourcolor)
	if hour == 6:
		for x in xrange(11, 16):
			strip.setPixelColor(x, off)
		for x in xrange(6, 11):
			strip.setPixelColor(x, hourcolor)
	if hour == 7:
		for x in xrange(6, 11):
			strip.setPixelColor(x, off)
		for x in xrange(1, 6):
			strip.setPixelColor(x, hourcolor)
	if hour == 8:
		for x in xrange(1, 6):
			strip.setPixelColor(x, off)
		for x in xrange(56, 61):
			strip.setPixelColor(x, hourcolor)
	if hour == 9:
		for x in xrange(56, 61):
			strip.setPixelColor(x, off)
		for x in xrange(51, 56):
			strip.setPixelColor(x, hourcolor)
	if hour == 10:
		for x in xrange(51, 56):
			strip.setPixelColor(x, off)
		for x in xrange(46, 51):
			strip.setPixelColor(x, hourcolor)
	if hour == 11:
		for x in xrange(46, 51):
			strip.setPixelColor(x, off)
		for x in xrange(41, 46):
			strip.setPixelColor(x, hourcolor)
	if hour == 12:
		for x in xrange(41, 46):
			strip.setPixelColor(x, off)
		for x in xrange(36, 41):
			strip.setPixelColor(x, hourcolor)
	
	if minute != second:
		strip.setPixelColor(minute, minutecolor)
	
	strip.setPixelColor(second, secondcolor)
	strip.show()
	lastsecond = second
	then = datetime.now()
	while then.second == now.second:
		then = datetime.now()

def snakemode(strip):
	global BUTTON_PRESSED
	wait_ms=100
	snakestart = random.randint(0, 59)
	apple = random.randint(0, 59)
	snakelength = 1
	while (snakestart == apple) or ((snakestart-1) == apple):
		apple = random.randint(0, 59)
	applecolor = Color(0, 255, 0) #Green
	snakecolor = Color(255, 0, 0) #Red
	snake = range(59)
	while True:
		if BUTTON_PRESSED == True:
			return
			
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0,0,0))
			
		if snakestart == apple:
			apple = random.randint(0, 59)
			snakelength += 1
			if snakelength > 58:
				snakelength = 1	
				
		for i in range(snakelength):
			if (snakestart-i) < 0:
				snake[i] = 60+(snakestart-i)
			else:
				snake[i] = snakestart-i

		x = 0
		while True:
			if snake[x] == apple:
				apple = random.randint(0, 59)
				x = 0
				continue
			x += 1
			if x > snakelength:
				break

		for i in range(snakelength):
			strip.setPixelColor(snake[i], wheel((i * 256 / snakelength) & 255))
		strip.setPixelColor(apple, applecolor)
		strip.show()
		time.sleep(wait_ms/1000.0)
		snakestart +=1
		if snakestart > 59:
			snakestart = 0
		
def cross(strip):
	wait_ms = 150.0
	global BUTTON_PRESSED
	for x in range(8):
		for i in range(8):
			strip.setPixelColor(x+7+i, wheel((((x+7+i) * 256 / (i+1)) & 255)))
			strip.setPixelColor(x+22+i, wheel((((x+22+i) * 256 / (i+1)) & 255)))
			strip.setPixelColor(x+37+i, wheel((((x+37+i) * 256 / (i+1)) & 255)))
			if (x+52+i) > 59:
				strip.setPixelColor((x+52+i)-60, wheel((((x+52+i) * 256 / (i+1)) & 255)))
			else:
				strip.setPixelColor(x+52+i, wheel((((x+52+i) * 256 / (i+1)) & 255)))
			strip.setPixelColor(x+7-i, wheel((((x+7-i) * 256 / (i+1)) & 255)))
			strip.setPixelColor(x+22-i, wheel((((x+22-i) * 256 / (i+1)) & 255)))
			strip.setPixelColor(x+37-i, wheel((((x+37-i) * 256 / (i+1)) & 255)))
			if (x+52-i) > 59:
				strip.setPixelColor((x+52-i)-60, wheel((((x+52-i) * 256 / (i+1)) & 255)))
			else:
				strip.setPixelColor(x+52-i, wheel((((x+52-i) * 256 / (i+1)) & 255)))
			strip.show()
			time.sleep(wait_ms/1000.0)
			if BUTTON_PRESSED == True:
				return
		for i in range(8):
			strip.setPixelColor(x+7+i, Color(0,0,0))
			strip.setPixelColor(x+22+i, Color(0,0,0))
			strip.setPixelColor(x+37+i, Color(0,0,0))
			if (x+52+i) > 59:
				strip.setPixelColor((x+52+i)-60, Color(0,0,0))
			else:
				strip.setPixelColor(x+52+i, Color(0,0,0))
			strip.setPixelColor(x+7-i, Color(0,0,0))
			strip.setPixelColor(x+22-i, Color(0,0,0))
			strip.setPixelColor(x+37-i, Color(0,0,0))
			if (x+52-i) > 59:
				strip.setPixelColor((x+52-i)-60, Color(0,0,0))
			else:
				strip.setPixelColor(x+52-i, Color(0,0,0))
			strip.show()
			time.sleep(wait_ms/1000.0)
			if BUTTON_PRESSED == True:
				return
		
############################################################################

def brightnessbutton(channel):
	global LED_BRIGHTNESS
	LED_BRIGHTNESS = LED_BRIGHTNESS + 51
	if LED_BRIGHTNESS > 255:
		LED_BRIGHTNESS = 51
	print("New Brightness: %s" % str(LED_BRIGHTNESS))
	strip.setBrightness(LED_BRIGHTNESS)
	strip.show()

def modebutton(channel):
	global MODE
	global BUTTON_PRESSED
	BUTTON_PRESSED = True
	MODE += 1
	if MODE > NUMBEROFMODES:
		MODE = 0
	print("New Mode: %s" % str(MODE))
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0, 0, 0))

############################################################################
    
# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	GPIO.add_event_detect(24, GPIO.RISING, callback=brightnessbutton, bouncetime=BOUNCETIME)
	GPIO.add_event_detect(23, GPIO.RISING, callback=modebutton, bouncetime=BOUNCETIME)

	astral = Astral()
	astral.solar_depression = 'civil'
	city = astral[CITY_NAME]
	print('Information for %s/%s\n' % (CITY_NAME, city.region))
	timezone = city.timezone
	print('Timezone: %s' % timezone)
	print('Latitude: %.02f; Longitude: %.02f\n' %(city.latitude, city.longitude))
	sun = city.sun(date=datetime.now(), local=True)
	print('Dawn:    %s' % str(sun['dawn']))
	print('Sunrise: %s' % str(sun['sunrise']))
	print('Noon:    %s' % str(sun['noon']))
	print('Sunset:  %s' % str(sun['sunset']))
	print('Dusk:    %s' % str(sun['dusk']))
	
	print("Infinity Mirror Started")

	print 'Press Ctrl-C to quit.'
	while True:
		if MODE == 0: #Clock Mode
			print("Starting Mode: %s" % str(MODE))
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, Color(0, 0, 0))
			while BUTTON_PRESSED == False:
				clock(strip, city) #start the clock
			BUTTON_PRESSED = False
		elif MODE == 1: 
			print("Starting Mode: %s" % str(MODE))
			while BUTTON_PRESSED == False:
				theaterChaseRainbow(strip)
			BUTTON_PRESSED = False
		elif MODE == 2:
			print("Starting Mode: %s" % str(MODE))
			while BUTTON_PRESSED == False:
				colorWipe(strip, Color(255, 0, 0))  # Red wipe
				colorWipe(strip, Color(0, 255, 0))  # Blue wipe
				colorWipe(strip, Color(0, 0, 255))  # Green wipe
			BUTTON_PRESSED = False
		elif MODE == 3:
			print("Starting Mode: %s" % str(MODE))
			while BUTTON_PRESSED == False:
				theaterChase(strip, Color(127, 127, 127))  # White theater chase
				theaterChase(strip, Color(127,   0,   0))  # Red theater chase
				theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
			BUTTON_PRESSED = False
		elif MODE == 4:
			print("Starting Mode: %s" % str(MODE))
			while BUTTON_PRESSED == False:
				rainbow(strip)
			BUTTON_PRESSED = False
		elif MODE == 5:
			print("Starting Mode: %s" % str(MODE))
			while BUTTON_PRESSED == False:
				rainbowCycle(strip)
			BUTTON_PRESSED = False
		elif MODE == 6: #Demo Mode
			print("Starting Mode: %s" % str(MODE))
			while BUTTON_PRESSED == False:
				# Color wipe animations.
				colorWipe(strip, Color(255, 0, 0))  # Red wipe
				colorWipe(strip, Color(0, 255, 0))  # Blue wipe
				colorWipe(strip, Color(0, 0, 255))  # Green wipe
				# Theater chase animations.
				theaterChase(strip, Color(127, 127, 127))  # White theater chase
				theaterChase(strip, Color(127,   0,   0))  # Red theater chase
				theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
				# Rainbow animations.
				rainbow(strip)
				rainbowCycle(strip)
				theaterChaseRainbow(strip)
			BUTTON_PRESSED = False
		elif MODE == 7: #Snake Mode
			print("Starting Mode: %s" % str(MODE))
			while BUTTON_PRESSED == False:
				snakemode(strip)
			BUTTON_PRESSED = False
		elif MODE == 8: #cross Mode
			print("Starting Mode: %s" % str(MODE))
			while BUTTON_PRESSED == False:
				cross(strip)
			BUTTON_PRESSED = False
		else:
			# Color wipe animations.
			colorWipe(strip, Color(255, 0, 0))  # Red wipe
			colorWipe(strip, Color(0, 255, 0))  # Blue wipe
			colorWipe(strip, Color(0, 0, 255))  # Green wipe
			# Theater chase animations.
			theaterChase(strip, Color(127, 127, 127))  # White theater chase
			theaterChase(strip, Color(127,   0,   0))  # Red theater chase
			theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
			# Rainbow animations.
			rainbow(strip)
			rainbowCycle(strip)
			theaterChaseRainbow(strip)
