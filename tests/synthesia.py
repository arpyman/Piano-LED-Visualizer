import mido
from mido import MidiFile, Message, tempo2bpm, MidiTrack,MetaMessage

from neopixel import *
import argparse
import time
import RPi.GPIO as GPIO

def find_between(s, start, end):
    try:
        return (s.split(start))[1].split(end)[0]
    except:
        return False
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)
# Main program logic follows:
if __name__ == '__main__':
	# LED strip configuration:
	LED_COUNT      = 144     # Number of LED pixels.
	LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
	#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
	LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
	LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
	LED_BRIGHTNESS = 30     # Set to 0 for darkest and 255 for brightest
	LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
	LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
	args = parser.parse_args()

	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	# Initialize the library (must be called once before other functions).
	strip.begin()

	ports = mido.get_input_names()



	for port in ports:
		if "Through" not in port and "RPiD" not in port and "RtMidOut" not in port:
			try:
				inport =  mido.open_input(port)
				print("In-port set to "+port)
			except:
				print ("Failed to set "+port+" as in-port")



	try:
		while True:
			for msg in inport.iter_pending():
				green = 0
				red = 0
				blue = 0
				#print(msg)
				note = find_between(str(msg), "note=", " ")
				original_note = note
				note = int(note)
				channel = int(find_between(str(msg), "channel=", " "))
				if "note_off" in str(msg):
					velocity = 0
				else:
					velocity = 100#find_between(str(msg), "velocity=", " ")
				#changing offset to adjust the distance between the LEDs to the key spacing
				if(note < 57):
					note_offset = 0
				elif(note > 72):
					note_offset = 2
				else:
					note_offset = 1
				if("note_on" in str(msg)):
					if(channel == 11):
						green = 0
						blue = 255
					elif(channel == 12):
						green = 255
						blue = 0
				vel = velocity#int(velocity)
				if(vel == 0 and int(note) > 0):
					#print("note: {0}".format(note))
					strip.setPixelColor(((note - 36)*2 - note_offset), Color(0, 0, 0))
				elif(vel > 0 and int(note) > 0):
					strip.setPixelColor(((note - 36)*2 - note_offset), Color(green*vel/127,red*vel/127,blue*vel/127))
			strip.show()
	except KeyboardInterrupt:
			if args.clear:
				colorWipe(strip, Color(0,0,0), 10)
