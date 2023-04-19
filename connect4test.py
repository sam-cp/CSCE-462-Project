import time
import random
import subprocess

moveseries = ""
gameboard = [[0 for i in range(6)] for j in range(7)]
current_player = 1

def button_press(btn):
    global gameboard, current_player, moveseries
    try:
        index = gameboard[btn].index(0)
    except ValueError:
        return
    gameboard[btn][index] = current_player
    moveseries += str(btn + 1)
    
    current_player = -current_player


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

def print_board(gb):
    for row in range(5, -1, -1):
        for col in range(7):
            if gb[col][row] > 0:
                print("x", end="")
            elif gb[col][row] < 0:
                print("o", end="")
            else:
                print(" ", end="")
        print()

def reset_game():
    global gameboard, current_player, moveseries
    gameboard = gameboard = [[0 for i in range(6)] for j in range(7)]
    current_player = 1
    moveseries = ""

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

while True:
    button_press(int(input("Move: ")) - 1)
    # print_board(gameboard)
    if (check_win(gameboard)):
        print_board(gameboard)
        print("%s Won!" % ("O" if current_player == 1 else "X"))
        reset_game()
        continue
    button_press(next_move(gameboard, moveseries))
    print_board(gameboard)
    if (check_win(gameboard)):
        print("%s Won!" % ("O" if current_player == 1 else "X"))
        reset_game()

    