import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

BTN = 22
GPIO.setup([BTN], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def button_press(arg):
	print("Button pressed")

GPIO.add_event_detect(BTN, GPIO.BOTH, button_press)

input()

