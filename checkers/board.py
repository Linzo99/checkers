import pygame
from .constants import BLACK, ROWS, COLS, SQUARE_SIZE, RED, WHITE
from .pieces import Piece
from collections import defaultdict

class Board:
	def __init__(self):
		self.board = []
		self.white_left = self.red_left = 12
		self.red_kings = self.white_kings = 0
		self.create_board()

	def draw_squares(self, win):
		win.fill(BLACK)
		for row in range(ROWS):
			for col in range(row%2, ROWS, 2):
				pygame.draw.rect(win, RED, (row*SQUARE_SIZE,col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

	def create_board(self):
		for row in range(ROWS):
			self.board.append([])
			for col in range(COLS):
				if col%2 == (row + 1) % 2:
					if row < 3:
						self.board[row].append(Piece(row, col, WHITE))
					elif  row > 4:
						self.board[row].append(Piece(row, col, RED))
					else:
						self.board[row].append(0)

				else:
					self.board[row].append(0)

	def remove(self, positions):
		for pos in positions:
			self.board[pos[0]][pos[1]] = 0

	def draw(self, win):
		self.draw_squares(win)
		for row in range(ROWS):
			for col in range(COLS):
				piece = self.board[row][col]
				if piece != 0:
					piece.draw(win)

	def move(self, piece, row, col):
		self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
		piece.move(row, col)

		if row == ROWS-1 or row == 0:
			piece.make_king()
			if piece.color == WHITE:
				self.white_kings += 1
			else:
				self.red_kings += 1

	def get_piece(self, row, col):
		return self.board[row][col]

	def is_empty(self, row, col):
		if(0<=row<=7) and (0<=col<=7):
			return self.board[row][col] == 0
		return None

	def get_valid_moves(self, piece, fstmove=True, skipped=[]):
		all_moves = {}
		left_moves = self.check_case_moves(piece, fstmove, -1, skipped)
		right_moves = self.check_case_moves(piece, fstmove, +1, skipped)
		all_moves.update(right_moves)
		all_moves.update(left_moves)

		return all_moves

	def check_case_moves(self, piece, fstmove, direc, skipped):
		row_col = (piece.row,piece.col)
		case = self.get_next_case(row_col, piece.direction, direc)
		if fstmove: skipped=[]
		moves = defaultdict(list)
		if piece.king:
			if fstmove:
				clone = Piece(*row_col, piece.color)
				clone.direction = -clone.direction
				clone.make_king()
				behind_moves = self.get_valid_moves(clone, False)
				moves.update(behind_moves)
			killed = []
			while case:
				if self.is_empty(*case):
					moves[case]
					if killed:
						moves[case].extend(killed)
						to_add = self.check_rev_diagonal(piece, case, killed)
						moves.update(to_add)

				elif not self.is_empty(*case) and self.get_piece(*case).color != piece.color:
					next_case = self.get_next_case(case, piece.direction, direc)
					if next_case and self.is_empty(*next_case):
						killed.append(case)
					else:
						break
				else:
					break

				case = self.get_next_case(case, piece.direction, direc)

		else:
			if case:
				if self.is_empty(*case) and fstmove:
					moves[case]

				elif not self.is_empty(*case) and self.get_piece(*case).color != piece.color:
					next_case = self.get_next_case(case, piece.direction, direc)
					if next_case and self.is_empty(*next_case):
						skip = self.get_piece(*case)
						row_s, col_s = skip.y // SQUARE_SIZE, skip.x // SQUARE_SIZE
						skipped.append((row_s, col_s))
						skipped = list(set(skipped))
						moves[next_case].extend(skipped)
						TestPiece = Piece(*next_case, piece.color)
						other_moves = self.get_valid_moves(TestPiece, False, skipped)
						moves.update(other_moves)
		return moves

	def get_next_case(self, case, row_direc, col_direc):
		next_case = (case[0]+row_direc, case[1]+col_direc) 
		if (0<=next_case[0]<=7) and (0<=next_case[1]<=7):
			return next_case 
		return None

	def check_rev_diagonal(self, piece, case, killed=None):
		to_return = dict()
		row, col = piece.y // SQUARE_SIZE, piece.x // SQUARE_SIZE
		row1, col1 = case
		if (row1 > row and col1>col) or (row1 < row and col1 < col):
			if piece.direction == +1 :
				down_moves = self.check_diagonal(piece, case, piece.direction, -1, killed)
				up_moves = self.check_diagonal(piece, case, -piece.direction, 1, killed)
			else:
				down_moves = self.check_diagonal(piece, case, piece.direction, 1, killed)
				up_moves = self.check_diagonal(piece, case, -piece.direction, -1, killed)

		elif (row1 < row and col1 > col) or (row1 > row and col1 < col):
			if piece.direction == +1:
				down_moves = self.check_diagonal(piece, case, -piece.direction, -1, killed)
				up_moves = self.check_diagonal(piece, case, piece.direction, 1, killed)
			else:
				down_moves = self.check_diagonal(piece, case, piece.direction, -1, killed)
				up_moves = self.check_diagonal(piece, case, -piece.direction, 1, killed)

		to_return.update(down_moves)
		to_return.update(up_moves)
		return to_return

	def check_diagonal(self, piece, case, row_dir, col_dir, killed):
		to_check = self.get_next_case(case, row_dir, col_dir)
		checked = defaultdict(list)
		while to_check:
			if not self.is_empty(*to_check) and piece.color != self.get_piece(*to_check).color:
				next_case = self.get_next_case(to_check, row_dir, col_dir)
				if next_case and self.is_empty(*next_case):
					killed.append(to_check)
					checked[next_case].extend(killed)
					TestPiece = Piece(*to_check, piece.color)
					other_moves = self.check_rev_diagonal(TestPiece, next_case, killed)
					checked.update(other_moves)
				else:
					break

			elif not self.is_empty(*to_check) and piece.color == self.get_piece(*to_check).color:
				break

			to_check = self.get_next_case(to_check, row_dir, col_dir)

		return checked

