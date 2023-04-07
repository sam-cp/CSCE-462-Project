import board
import neopixel
import RPi.GPIO as GPIO
import time
import random

gameboard = [[0 for i in range(6)] for j in range(7)]
current_player = 1

def button_press(btn):
	global gameboard, current_player
	try:
		index = gameboard[btn].index(0)
	except ValueError:
		return
	gameboard[btn][index] = current_player
	won = check_win(gameboard)
	if won:
		for i in range(50):
			update_lights()
			time.sleep(0.1)
		pixels.fill(0)
		pixels.show()
		gameboard = [[0 for i in range(6)] for j in range(7)]
		current_player = 1
	else:
		current_player = -current_player
		update_lights()


def check_win(gb):
	# Check horizontal win -
	for col in range(4):
		for row in range(6):
			if gb[col][row] == 0:
				continue
			all_same = True
			for i in range(1, 4):
				if gb[col + i][row] != gb[col][row]:
					all_same = False
					break
			if all_same:
				for i in range(4):
					gb[col + i][row] *= 2
				return True
	
	
	# Check vertical |
	for col in range(7):
		for row in range(3):
			if gb[col][row] == 0:
				continue
			all_same = True
			for i in range(1, 4):
				if gb[col][row + i] != gb[col][row]:
					all_same = False
					break
			if all_same:
				for i in range(4):
					gb[col][row + i] *= 2
				return True
	
	# Check diagonal /
	for col in range(4):
		for row in range(3):
			if gb[col][row] == 0:
				continue
			all_same = True
			for i in range(1, 4):
				if gb[col + i][row + i] != gb[col][row]:
					all_same = False
					break
			if all_same:
				for i in range(4):
					gb[col + i][row + i] *= 2
				return True
	
	# Check diagonal \
	for col in range(3, 7):
		for row in range(3):
			if gb[col][row] == 0:
				continue
			all_same = True
			for i in range(1, 4):
				if gb[col - i][row + i] != gb[col][row]:
					all_same = False
					break
			if all_same:
				for i in range(4):
					gb[col - i][row + i] *= 2
				return True
	return False



# Hardware setup

pixels = neopixel.NeoPixel(board.D18, 64, brightness=0.1, pixel_order=neopixel.GRB, auto_write=False)
pixels.fill(0);
pixels.show()

BUTTONS = [
	23,
	24,
	25,
	12,
	16,
	20,
	21
]

GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

last_press = time.time()
COOLDOWN = 0.5

def button_callback(btn):
	global last_press
	print("Pressed")
	if time.time() - last_press >= COOLDOWN:
		last_press = time.time()
		button_press(BUTTONS.index(btn))

def update_lights():
	global gameboard
	for i in range(42):
		column = i // 6
		row = i % 6
		pixelindex = (7 - row) * 8 + column
		if gameboard[column][row] > 0:
			if gameboard[column][row] == 2 and time.time() % 1 < 0.5:
				pixels[pixelindex] = [0, 255, 0]
			else:
				pixels[pixelindex] = [255, 0, 0]
		elif gameboard[column][row] < 0:
			if gameboard[column][row] == -2 and time.time() % 1 < 0.5:
				pixels[pixelindex] = [0, 255, 0]
			else:
				pixels[pixelindex] = [255, 255, 0]
		else:
			pixels[pixelindex] = [0, 0, 0]
	pixels.show()

for i in BUTTONS:
	GPIO.add_event_detect(i, GPIO.RISING, button_callback)

input()

pixels.fill(0)
pixels.show()
