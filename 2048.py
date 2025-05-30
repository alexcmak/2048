import sys
import pygame
import random
import pygame_menu
from pygame_menu import themes

# 2048 game by Alex Mak
# This is my slightly more readable version of this excellent program.
# my thanks to the original programmer
# from https://github.com/DBgirl/PyGames/blob/main/5_2048/2048.py
pygame.init()

DIM = 4  # dimension - number of tiles across and up/down
TILE_SIZE = 100
GAP_SIZE = 15
MARGIN = 20
WIN_SCORE = 2048  # should be power of 2

BACKGROUND_COLOR = (255, 251, 240)
EMPTY_TILE_COLOR = (205, 192, 180)
TILE_COLORS = {
	2: (238, 228, 218),
	4: (237, 224, 200),
	8: (242, 177, 121),
	16: (245, 149, 99),
	32: (246, 124, 95),
	64: (246, 94, 59),
	128: (237, 207, 114),
	256: (237, 204, 97),
	512: (237, 200, 80),
	1024: (237, 197, 63),
	2048: (237, 194, 46)
}
FONT_COLOR = (0, 0, 0)
FONT = pygame.font.SysFont('arial', 40)

def draw_tile(screen, value, x, y):
	color = TILE_COLORS.get(value, (60, 58, 50))
	rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
	pygame.draw.rect(screen, color, rect)
	if value != 0:
		text = FONT.render(str(value), True, FONT_COLOR)
		text_rect = text.get_rect(center=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))
		screen.blit(text, text_rect)

def draw_board(screen, board):
	screen.fill(BACKGROUND_COLOR)
	for row in range(DIM):
		for col in range(DIM):
			value = board[row][col]
			x = MARGIN + col * (TILE_SIZE + GAP_SIZE)
			y = MARGIN + row * (TILE_SIZE + GAP_SIZE)
			draw_tile(screen, value, x, y)

def two_or_four():
	num_list = [2,4]
	return random.choice(num_list)

def add_new_tile(board):
	empty_tiles = [(r, c) for r in range(DIM) for c in range(DIM) if board[r][c] == 0]
	if empty_tiles:
		row, col = random.choice(empty_tiles)
		board[row][col] = two_or_four()

# this function shove tiles to the left and combine tiles where applicable
# this function is the base implementation of all move directions
def merge_row(row):
	row_len = len(row)
	new_row = [i for i in row if i != 0]
	new_row += [0] * (row_len - len(new_row))
	for i in range(row_len - 1):
		if new_row[i] == new_row[i + 1] and new_row[i] != 0:
			new_row[i] *= 2
			new_row[i + 1] = 0
	new_row = [i for i in new_row if i != 0]
	new_row += [0] * (row_len - len(new_row))
	return new_row

# merge every row to the left
def move_left(board):
	new_board = []
	for row in board:
		new_board.append(merge_row(row))
	return new_board

def move_right(board):
	new_board = []
	for row in board:

		reversed_row = row[::-1]
		merged_row = merge_row(reversed_row)

		new_board.append(merged_row[::-1]) # append unreversed row
	return new_board

def move_up(board):
	new_board = list(zip(*board))
	new_board = move_left(new_board)
	return [list(row) for row in zip(*new_board)]

# a move_down can be done with a move_right()
def move_down(board):
    # the paramater 'board' is a 2D array
    # list(zip()) make pairs into lists; essentially carving out each column into elements
    new_board = list(zip(*board))

    #  A, B, C, D
    #  E, F, G, H
    #  I, J, K, L
    #  M, N, O, P

    # new_board becomes [(A,E,I,M),(B,F,J,N),(C,G,K,O),(D,H,L,P)]

    new_board = move_right(new_board) # shift each element to the right, merge where applicable

    # this expression reconstitute the list back to 2D array
    return [list(row) for row in zip(*new_board)] 

def check_win(board):
	for row in board:
		if WIN_SCORE in row:
			return True
	return False

def check_moves_available(board):
	for row in range(DIM):
		if 0 in board[row]:
			return True
		for col in range(DIM - 1):
			if board[row][col] == board[row][col + 1]:
				return True
	for col in range(DIM):
		for row in range(DIM - 1):
			if board[row][col] == board[row + 1][col]:
				return True
	return False

def game():
	SCREEN_DIM = DIM * TILE_SIZE + (DIM-1) * GAP_SIZE + 2 * MARGIN
	screen = pygame.display.set_mode((SCREEN_DIM, SCREEN_DIM))
	pygame.display.set_caption(str(WIN_SCORE) + " Game - Alex Mak")
	clock = pygame.time.Clock()

	# list comprehension way to initialize a 2D square array
	board = [[0] * DIM  for _ in range(DIM)]
	add_new_tile(board)
	add_new_tile(board)

	running = True
	won = False
	lost = False
	global b_sound

	l_sound = b_sound

	win_sound = pygame.mixer.Sound("Sounds/wow.ogg")

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if not won and not lost:
					if event.key == pygame.K_LEFT:
						board = move_left(board)
					elif event.key == pygame.K_RIGHT:
						board = move_right(board)
					elif event.key == pygame.K_UP:
						board = move_up(board)
					elif event.key == pygame.K_DOWN:
						board = move_down(board)
					add_new_tile(board)
					won = check_win(board)
					lost = not check_moves_available(board)

		draw_board(screen, board)

		if won:
			text = FONT.render("You Won!", True, (255, 0, 0))
			text_rect = text.get_rect(center=(SCREEN_DIM // 2, SCREEN_DIM // 2))
			screen.blit(text, text_rect)

			if(l_sound):  # play just once
				pygame.mixer.Sound.play(win_sound)
				pygame.mixer.music.stop()
				l_sound = False 

		elif lost:
			text = FONT.render("You Lost!", True, (255, 0, 0))
			text_rect = text.get_rect(center=(SCREEN_DIM // 2, SCREEN_DIM // 2))
			screen.blit(text, text_rect)

		pygame.display.flip()
		clock.tick(30)

# ---------------------
# Menu

MENU_WIDTH = 600
MENU_HEIGHT = 400

difficult_value = "Hard"
def set_difficulty(value, score):
    global WIN_SCORE
    global difficult_value
    WIN_SCORE = score
    difficult_value = value[0][0]
 
def start_the_game():
    game()
    pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
 
def level_menu():
    mainmenu._open(level)

def size_menu():
    mainmenu._open(size)

def set_size(value, size):
    global DIM
    DIM = size
 
def draw_size_update_function(widget, menu):
    widget.set_title("Size: " + str(DIM))

def draw_level_update_function(widget, menu):
    widget.set_title("Level: " + difficult_value)

def sound_menu():
    mainmenu._open(sound)

b_sound = True
def set_sound(value, sound):
    global b_sound
    b_sound = sound;

def draw_sound_update_function(widget, menu):

    if (b_sound):
         widget.set_title("Sound: On")
    else:
        widget.set_title("Sound: Off")


def quit():
    pygame.quit()
    sys.exit(0)

pygame.display.set_caption(str(WIN_SCORE) + " Game - Alex Mak")
surface = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
mainmenu = pygame_menu.Menu('2048 Game', MENU_WIDTH, MENU_HEIGHT, theme=themes.THEME_SOLARIZED)
mainmenu.add.button('Play', start_the_game)

size_button = mainmenu.add.button('Size', size_menu)
size_button.add_draw_callback(draw_size_update_function)

level_button = mainmenu.add.button('Level', level_menu)
level_button.add_draw_callback(draw_level_update_function)

sound_button = mainmenu.add.button('Sound', sound_menu)
sound_button.add_draw_callback(draw_sound_update_function)

mainmenu.add.button('Quit', quit)
 
level = pygame_menu.Menu('Select a Difficulty', 600,400, theme=themes.THEME_BLUE)
level.add.selector('Difficulty :', [('Hard', 2048), ('Easy', 1024), ('Very Easy', 128)], onchange=set_difficulty)

size = pygame_menu.Menu('Select a Size', 600,400, theme=themes.THEME_BLUE)
size.add.selector('Size :', [('4', 4), ('5', 5), ('6', 6)], onchange=set_size)

sound = pygame_menu.Menu('Sound Effects', 600,400, theme=themes.THEME_BLUE)
sound.add.selector('Sound:', [('On', True), ('Off', False)], onchange=set_sound)

mainmenu.mainloop(surface)


