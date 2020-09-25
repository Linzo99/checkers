import pygame
from .constants import WHITE, SQUARE_SIZE, GREY, GREEN, CROWN, RED, BLACK

class Piece:
	PADDING = 15
	OUTLINE = 2
	def __init__(self, row, col, color):
		self.row = row
		self.col = col
		self.color = color
		self.king = False

		if color == WHITE:
			self.direction = +1
		else :
			self.direction = -1

		self.x = self.y = 0
		self.calc_pos()

	def calc_pos(self):
		self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
		self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

	def make_king(self):
		self.king = True
		

	def get_rev_color(self):
		if self.color == WHITE:
			return RED
		return WHITE

	def draw(self,win):
		radius = SQUARE_SIZE // 2 - self.PADDING
		pygame.draw.circle(win, GREEN, (self.x, self.y), radius+self.OUTLINE)
		pygame.draw.circle(win, self.color, (self.x, self.y), radius)
		if self.king:
			win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height()//2))
		else:
			pygame.draw.circle(win, GREY, (self.x, self.y), radius-5)
			pygame.draw.circle(win, self.color, (self.x, self.y), radius-7)

	def move(self, row, col):
		self.row = row
		self.col = col
		self.calc_pos()

	def __repr__(self):
		return f"[x:{self.row} y:{self.col}] direc:{self.direction} color:{self.color} isKing:{self.king}"
