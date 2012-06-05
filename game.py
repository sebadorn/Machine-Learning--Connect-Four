#!/usr/bin/python
# -*- encoding: utf-8 -*-

import numpy as ny
import mlp


FIELD_WIDTH = 7
FIELD_HEIGHT = 6
CONNECT = 4

STONE_BLANK = 0
STONE_HUMAN = 1
STONE_ANN = 2


class Game:
	""" Play a game of Connect Four. """


	def __init__( self, ann ):
		self.ann = ann
		self._init_field()


	def _init_field( self ):
		""" Init play field. """

		self.board = ny.zeros( ( FIELD_WIDTH, FIELD_HEIGHT ) )
		self.current_height = [0] * FIELD_WIDTH


	def input_valid( self, x ):
		""" Validates the chosen column x. """

		# Outside of game board width.
		if x < 0 or x > FIELD_WIDTH - 1:
			return False

		# Column is full.
		if self.current_height[x] >= FIELD_HEIGHT:
			return False

		return True


	def check_win( self ):
		""" Check the game board if someone has won.

		Returns the stone value of the winner.
		"""

		for x in range( FIELD_WIDTH ):
			for y in range( FIELD_HEIGHT ):
				stone = self.board[x][y]
				# We only care about players, not blank fields
				if stone == STONE_BLANK:
					continue

				# Look up
				for i in range( 1, CONNECT ):
					if y + i >= FIELD_HEIGHT:
						break
					# C-c-c-combo breaker!
					if stone != self.board[x][y + i]:
						break
					# All stones connected: Winner found!
					return stone

				# Look right
				for i in range( 1, CONNECT ):
					if x + i >= FIELD_WIDTH:
						break
					if stone != self.board[x + i][y]:
						break
					return stone

				# Look diagonal right
				for i in range( 1, CONNECT ):
					if x + i >= FIELD_WIDTH or y + i >= FIELD_HEIGHT:
						break
					if stone != self.board[x + i][y + i]:
						break
					return stone

				# Look diagonal left
				for i in range( 1, CONNECT ):
					if x - i < 0 or y + i >= FIELD_HEIGHT:
						break
					if stone != self.board[x - i][y + i]:
						break
					return stone

		return STONE_BLANK


	def check_board_full( self ):
		""" Returns true if there are no more free fields,
		false otherwise. """

		if ny.shape( ny.where( self.board == STONE_BLANK ) )[1] == 0:
			return True
		return False


	def play( self ):
		""" Start playing. """

		while 1:
			try:
				x = raw_input( ">> Column: " )
			except EOFError: print; break
			except KeyboardInterrupt: print; break

			# Validate user input
			x = int( x ) - 1
			if not self.input_valid( x ):
				print "No valid field position!"
				continue

			# Place human stone
			y = self.current_height[x]
			self.current_height[x] += 1
			self.board[x][y] = STONE_HUMAN

			winner = self.check_win()
			if winner == STONE_HUMAN:
				print "You won!"
				break
			elif winner == STONE_ANN:
				print "The ANN won!"
				break

			# Place ANN stone
			ann_board_format = []
			for i in range( FIELD_WIDTH ):
				ann_board_format.extend( self.board[i] )
			ann_output = self.ann.use( ann_board_format )
			print ann_output

			winner = self.check_win()
			if winner == STONE_HUMAN:
				print "You won!"
				break
			elif winner == STONE_ANN:
				print "The ANN won!"
				break

			# Draw
			if self.check_board_full():
				print "No more free fields. It's a draw!"
				break

		print "Game ended."



if __name__ == "__main__":
	# Small test
	g = Game( None )
	print "Well, nothing crashed …"