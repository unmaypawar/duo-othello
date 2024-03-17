from tkinter import *


from engine import get_moves, update_board, killer_move
from minimax import max_node


class Board:
	def __init__(self):
		self.player = 0
		self.passed = False
		self.over = False

		self.array = []
		for i in range(board_length):
			temp_array = []
			for j in range(board_length):
				temp_array.append('.')
			self.array.append(temp_array)

		self.array[2][3] = 'B'
		self.array[3][2] = 'B'
		self.array[8][9] = 'B'
		self.array[9][8] = 'B'
		self.array[2][2] = 'W'
		self.array[3][3] = 'W'
		self.array[8][8] = 'W'
		self.array[9][9] = 'W'


	def update(self):
		player_moves = get_moves(self.array, board_length, 'W', 'B')

		screen.delete('pieces')
		for i in range(board_length):
			for j in range(board_length):
				x1, y1 = j * 50, (i+1) * 50
				x2, y2 = x1 + 50, y1 + 50
				screen.create_rectangle(x1, y1, x2, y2, fill = 'green', tags = 'pieces')
				if self.array[i][j] == 'B':
					screen.create_oval(x1+4, y1+4, x2-4, y2-4, fill = 'black', tags = 'pieces')
				elif self.array[i][j] == 'W':
					screen.create_oval(x1+4, y1+4, x2-4, y2-4, fill = 'white', tags = 'pieces')
				elif self.player == 0 and (i, j) in player_moves:
					screen.create_oval(x1+4, y1+4, x2-4, y2-4, tags = 'pieces')
		screen.update()

		if not self.over:
			self.draw_scoreboard()
			screen.update()

			if self.player == 1:
				best_move = killer_move(self.array, board_length, 'B', 'W')
				if best_move == None:
					best_score, best_move = max_node(self.array, board_length, depth, float('-inf'), float('inf'), 'B', 'W')

				if best_move == None:
					self.passed = True
				else:
					self.array = update_board(self.array, board_length, 'B', best_move)
					self.player = 1 - self.player
					self.pass_check()

		else:
			screen.delete('score')
			player_score_int = 0
			ai_score_int = 0
			for i in range(board_length):
				for j in range(board_length):
					if self.array[i][j] == 'W':
						player_score_int += 1
					elif self.array[i][j] == 'B':
						ai_score_int += 1

			player_score = 'Player ' + str(player_score_int)
			ai_score = 'AI ' + str(ai_score_int)

			screen.create_text(100, 25, anchor = 'w', tags = 'score', font = ('San Francisco', 40), fill = 'white', text = player_score)
			screen.create_text(400, 25, anchor = 'w', tags = 'score', font = ('San Francisco', 40), fill = 'black', text = ai_score)

			if player_score_int > ai_score_int:
				screen.create_text(300 ,350, anchor = 'c', font = ('San Francisco', 40), fill = 'red', text = 'Winner: Player')
			elif player_score_int < ai_score_int:
				screen.create_text(300 ,350, anchor = 'c', font = ('San Francisco', 40), fill = 'red', text = 'Winner: AI')
			else:
				screen.create_text(300 ,350, anchor = 'c', font = ('San Francisco', 40), fill = 'red', text = 'Game Tie')


	def make_move(self, row, col):
		self.array = update_board(self.array, board_length, 'W', (row, col))

		self.player = 1 - self.player
		self.update()

		self.pass_check()
		self.update()


	def draw_scoreboard(self):
		screen.delete('score')

		player_score_int = 0
		ai_score_int = 0

		for i in range(board_length):
			for j in range(board_length):
				if self.array[i][j] == 'W':
					player_score_int += 1
				elif self.array[i][j] == 'B':
					ai_score_int += 1

		player_score = 'Player ' + str(player_score_int)
		ai_score = 'AI ' + str(ai_score_int)

		screen.create_text(100, 25, anchor = 'w', tags = 'score', font = ('San Francisco', 40), fill = 'white', text = player_score)
		screen.create_text(400, 25, anchor = 'w', tags = 'score', font = ('San Francisco', 40), fill = 'black', text = ai_score)


	def pass_check(self):
		must_pass = True

		if self.player == 0:
			moves = get_moves(self.array, board_length, 'W', 'B')
		else:
			moves = get_moves(self.array, board_length, 'B', 'W')
		if moves:
			must_pass = False

		if must_pass:
			self.player = 1 - self.player
			if self.passed == True:
				self.over = True
			else:
				self.passed = True
			self.update()
		else:
			self.passed = False


def handle_click(event):
	if board.player == 0:
		col = event.x // 50
		row = event.y // 50 - 1
		player_moves = get_moves(board.array, board_length, 'W', 'B')
		if (row, col) in player_moves:
			board.make_move(row, col)


depth = 4
board_length = 12


root = Tk()
screen = Canvas(root, width = 600, height = 650, bg = 'lightblue')
screen.pack()


board = Board()
board.update()


screen.bind("<Button-1>", handle_click)
root.title('Duo-Othello')
root.mainloop()