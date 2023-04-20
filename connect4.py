import board
import neopixel
import RPi.GPIO as GPIO
import time
import random
import subprocess
import threading

two_player = True
gameboard = []
current_player = 1
move_series = ""
COOLDOWN = 0.5
can_press_button = threading.Lock()
game_started = False

def button_press(btn):
	global gameboard, current_player, move_series, game_started
	try:
		index = gameboard[btn].index(0)
	except ValueError:
		return
	gameboard[btn][index] = current_player
	move_series += str(btn + 1)
	won = check_win(gameboard)
	if won:
		for i in range(10):
			update_lights()
			time.sleep(0.5)
		game_started = False
		update_lights()
	else:
		current_player = -current_player
		update_lights()
		if (not two_player):
			if current_player == 1:
				button_press(next_move(gameboard, move_series))
		else:
			if len(move_series) == 42:
				time.sleep(5)
				game_started = False
				update_lights()

def get_solution(ms):
    try:
        output = subprocess.check_output(["./solver/a.out", ms], stderr=subprocess.STDOUT, timeout=0.5)
        return int(output.decode())
    except subprocess.TimeoutExpired:
        return 0

def next_move(gb, ms):
    min_score = 21
    min_columns = []
    for i in range(7):
        try:
            gb[i].index(0)
        except ValueError:
            continue
        sol = get_solution(ms + str(i + 1))
        if sol == min_score:
            min_columns.append(i)
        elif sol < min_score:
            min_score = sol
            min_columns = [i]
    return random.choice(min_columns)

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

def start_game(tp):
	global two_player, gameboard, current_player, move_series
	two_player = tp
	gameboard = [[0 for i in range(6)] for j in range(7)]
	current_player = 1
	move_series = ""
	update_lights()

# Hardware setup

pixels = neopixel.NeoPixel(board.D18, 64, brightness=0.1, pixel_order=neopixel.GRB, auto_write=False)
pixels.fill(0)
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

def button_callback(btn):
	global last_press, game_started
	print("Pressed")
	if time.time() - last_press >= COOLDOWN:
		last_press = time.time()
		idx = BUTTONS.index(btn)
		if (can_press_button.locked()):
			return
		can_press_button.acquire()
		if game_started:
			button_press()
		elif idx == 0 or idx == 6:
			start_game(False)
		can_press_button.release()

def update_lights():
	global gameboard, pixels, game_started
	if game_started:
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
	else:
		pixels.fill([0, 64, 128])
	pixels.show()

for i in BUTTONS:
	GPIO.add_event_detect(i, GPIO.RISING, button_callback)

input()

pixels.fill(0)
pixels.show()
