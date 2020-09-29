from copy import deepcopy
import pygame
from checkers.constants import WHITE, RED

def minimax(board, depth, ismax):
	if depth == 0 or board.iswinner():
		return board.evaluate(), board

	if ismax:
		maxEval = float('-inf')
		best_pos = None
		for pos in get_possible_moves(board, WHITE):
			evaluation, b = minimax(pos, depth-1,False)
			maxEval = max(maxEval, evaluation)
			if maxEval == evaluation:
				best_pos = pos
		return maxEval, best_pos

	else:
		minEval = float('inf')
		best_pos = None
		for pos in get_possible_moves(board, RED):
			evaluation, b = minimax(pos, depth-1,True)
			minEval = min(minEval, evaluation)
			if minEval == evaluation:
				best_pos = pos
		return minEval, best_pos




def get_possible_moves(board, color):
	boards = []
	for piece in board.get_moving_pieces(color):
		moves = board.get_valid_moves(piece)
		for pos, killed in moves.items():
			cp_board = deepcopy(board)
			cp_piece = cp_board.get_piece(piece.row, piece.col)
			cp_board.move(cp_piece, *pos)
			if killed:
				cp_board.remove(killed)
			boards.append(cp_board)

	return boards