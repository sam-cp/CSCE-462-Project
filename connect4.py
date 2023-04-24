import board
import neopixel
import RPi.GPIO as GPIO
import time
import random
import subprocess
import threading

COLOR_RED = (128, 0, 0)
COLOR_RED_DARK = (64, 0, 0)
COLOR_YELLOW = (128, 64, 0)
COLOR_YELLOW_DARK = (64, 32, 0)
COLOR_GREEN_BRIGHT = (0, 255, 0)
COLOR_GREEN_DARK = (0, 64, 0)
COLOR_BLUE_BRIGHT = (0, 128, 255)
COLOR_BLUE_DARK = (0, 32, 64)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (16, 16, 16)

two_player = True
gameboard = []
current_player = 1
move_series = ""
COOLDOWN = 0.5
can_press_button = threading.Lock()
game_started = False

def button_press(btn):
	global gameboard, current_player, move_series, game_started, can_press_button
	if game_started:
		if not drop_piece(btn, gameboard, current_player):
			flash_col(btn, gameboard)
			can_press_button.release()
			return
		move_series += str(btn + 1)
		won = check_win(gameboard)
		if won:
			for i in range(10):
				update_lights()
				time.sleep(0.5)
			game_started = False
			update_lights()
			can_press_button.release()
		else:
			current_player = -current_player
			update_lights()
			if (not two_player):
				if current_player == -1:
					button_press(next_move(gameboard, move_series))
				else:
					can_press_button.release()
			else:
				if len(move_series) == 42:
					time.sleep(5)
					game_started = False
					update_lights()
				can_press_button.release()
	else:
		if btn == 0:
			start_game(False)
		elif btn == 6:
			start_game(True)
		can_press_button.release()

def flash_col(col, gb):
	for i in range(6):
		gb[col][i] *= 3
		time.sleep(0.025)
		update_lights()
	time.sleep(0.2)
	for i in range(6):
		gb[col][i] //= 3
		time.sleep(0.025)
		update_lights()

def drop_piece(col, gb, cp):
	if gb[col][5] != 0:
		return False
	gb[col][5] = cp
	row = 4
	while row >= 0 and gb[col][row] == 0:
		update_lights()
		gb[col][row + 1] = 0
		gb[col][row] = cp
		time.sleep(0.05)
		row -= 1
	return True

def get_solution(ms):
	try:
		output = subprocess.check_output(["/home/admin/Project/solver/a.out", ms], stderr=subprocess.STDOUT, timeout=3/7)
		print("Done!")
		return int(output.decode())
	except subprocess.TimeoutExpired:
		print("Timed out");
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
	global two_player, gameboard, current_player, move_series, game_started
	two_player = tp
	gameboard = [[0 for i in range(6)] for j in range(7)]
	current_player = 1
	move_series = ""
	game_started = True
	update_lights()

# Hardware setup

pixels = neopixel.NeoPixel(board.D10, 64, brightness=0.1, pixel_order=neopixel.GRB, auto_write=False)
pixels.fill(COLOR_BLACK)
pixels.show()

BUTTONS = [
	27,
	22,
	5,
	6,
	13,
	19,
	26
]

GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

last_press = time.time()

def button_callback(btn):
	global last_press
	idx = BUTTONS.index(btn)
	if time.time() - last_press >= COOLDOWN:
		last_press = time.time()
		if (can_press_button.locked()):
			return
		can_press_button.acquire()
		print("Actually pushed", idx)
		t = threading.Thread(target=button_press, args=[idx], daemon=True)
		t.start()

def update_lights():
	global gameboard, pixels, game_started
	pixels.fill(0)
	if game_started:
		pixels[0] = COLOR_RED_DARK
		pixels[1] = COLOR_BLUE_DARK
		pixels[2] = COLOR_GREEN_DARK
		pixels[3] = COLOR_BLUE_DARK
		pixels[4] = COLOR_GREEN_DARK
		pixels[5] = COLOR_BLUE_DARK
		pixels[6] = COLOR_YELLOW_DARK
		for i in range(7, 64, 8):
			pixels[i] = COLOR_GRAY
		for i in range(42):
			column = i // 6
			row = i % 6
			pixelindex = (7 - row) * 8 + column
			if gameboard[column][row] == 3 or gameboard[column][row] == -3:
				pixels[pixelindex] = COLOR_BLUE_BRIGHT
			elif gameboard[column][row] > 0:
				if gameboard[column][row] == 2 and time.time() % 1 < 0.5:
					pixels[pixelindex] = COLOR_GREEN_BRIGHT
				else:
					pixels[pixelindex] = COLOR_RED
			elif gameboard[column][row] < 0:
				if gameboard[column][row] == -2 and time.time() % 1 < 0.5:
					pixels[pixelindex] = COLOR_GREEN_BRIGHT
				else:
					pixels[pixelindex] = COLOR_YELLOW
			else:
				pixels[pixelindex] = COLOR_BLACK
	else:
		ON_RED = [9, 17, 25, 33, 41, 49]
		ON_YELLOW = [12, 13, 14, 22, 30, 29, 28, 36, 44, 52, 53, 54]
		for i in ON_RED:
			pixels[i] = COLOR_RED
		for i in ON_YELLOW:
			pixels[i] = COLOR_YELLOW
			
	pixels.show()

for i in BUTTONS:
	GPIO.add_event_detect(i, GPIO.RISING, button_callback)

update_lights()

# while True:
#   inp = int(input())
#   print(game_started)
#   button_press(inp - 1)

while True:
  time.sleep(60)
