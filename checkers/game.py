import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board
from minimax.algo import minimax

class Game:
	def __init__(self, win):
		self._init()
		self.win = win

	def update(self):
		self.board.draw(self.win)
		self.draw_valid_moves(self.valid_moves)
		pygame.display.update()

	def _init(self):
		self.selected = None
		self.board = Board()
		self.turn = WHITE
		self.valid_moves = {}

	def reset(self):
		self._init()


	def on_case_click(self, row, col):
		if self.selected:
			result = self._move(row, col)
			if not result:
				self.selected = None
				self.on_case_click(row, col)

		piece = self.board.get_piece(row, col)
		if piece != 0 and piece.color == self.turn:
			self.selected = piece
			self.valid_moves = self.board.get_valid_moves(piece)
			#print(self.valid_moves)
			return True

		return False

	def _move(self, row, col):
		piece = self.board.get_piece(row, col)
		if self.selected and piece == 0 and (row, col) in self.valid_moves:
			self.board.move(self.selected, row, col)
			self.change_turn()
			self.selected = None
			skipped = self.valid_moves[(row, col)]
			self.valid_moves = {}
			if skipped:
				self.board.remove(skipped)
		else:
			return False

		return True

	def draw_valid_moves(self, moves):
		for move in moves:
			row, col = move
			pygame.draw.circle(self.win, BLUE, (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2), 12)


	def change_turn(self):
		if self.turn == RED:
			self.turn = WHITE
		else:
			self.turn = RED

	def ai_move(self):
		sc, board = minimax(self.board, 3, True)
		self.board = board

	def get_board(self):
		return self.board