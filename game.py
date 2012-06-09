#!/usr/bin/python
# -*- encoding: utf-8 -*-

from global_vars import *
import sys, random, numpy as ny
import mlp


class Game:
	""" Play a game of Connect Four. """


	def __init__( self, ai ):
		self.ai = ai
		self._init_field()


	def _init_field( self ):
		""" Init play field. """

		self.board = ny.array( [[STONE_BLANK] * FIELD_HEIGHT] * FIELD_WIDTH )
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

		count = 0
		for x in range( FIELD_WIDTH ):
			for y in range( FIELD_HEIGHT ):
				stone = self.board[x][y]
				# We only care about players, not blank fields
				if stone == STONE_BLANK:
					count = 0; continue

				# Look up
				for i in range( 1, CONNECT ):
					if y + i >= FIELD_HEIGHT:
						count = 0; break
					# C-c-c-combo breaker!
					if stone != self.board[x][y + i]:
						count = 0; break
					count += 1
				# All stones connected: Winner found!
				if count + 1 == CONNECT:
					return stone

				# Look right
				for i in range( 1, CONNECT ):
					if x + i >= FIELD_WIDTH:
						count = 0; break
					if stone != self.board[x + i][y]:
						count = 0; break
					count += 1
				if count + 1 == CONNECT:
					return stone

				# Look diagonal right
				for i in range( 1, CONNECT ):
					if x + i >= FIELD_WIDTH or y + i >= FIELD_HEIGHT:
						count = 0; break
					if stone != self.board[x + i][y + i]:
						count = 0; break
					count += 1
				if count + 1 == CONNECT:
					return stone

				# Look diagonal left
				for i in range( 1, CONNECT ):
					if x - i < 0 or y + i >= FIELD_HEIGHT:
						count = 0; break
					if stone != self.board[x - i][y + i]:
						count = 0; break
					count += 1
				if count + 1 == CONNECT:
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

		x_range = range( FIELD_WIDTH )

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

			self.print_board( self.board )

			winner = self.check_win()
			if winner == STONE_HUMAN:
				print "You won!"
				break
			elif winner == STONE_AI:
				print "The ai won!"
				break

			# Place ai stone
			pos_win = { "col": 0, "out": 0 }
			pos_draw = { "col": 0, "out": 0 }
			pos_loss = { "col": 0, "out": 0 }

			random.shuffle( x_range )
			for x in x_range:
				# Cell (y) in this column (x) we are currently testing
				y = self.current_height[x]
				if y >= FIELD_HEIGHT:
					continue

				# Don't change the real game board
				board_copy = self.board.copy()
				board_copy[x][y] = STONE_AI

				# Array format for the ai: 7x6 -> 1x42
				ai_board_format = []
				for i in range( FIELD_WIDTH ):
					ai_board_format.extend( board_copy[i] )

				# Get the possible outcome
				ai_output = self.ai.use( ai_board_format )[0][0]
				print x, ai_output

				if round( ai_output ) == WIN:
					diff_new = WIN - ai_output
					diff_old = WIN - pos_win["out"]
					pos_win["col"] = x if diff_new < diff_old else pos_win["col"]
				elif round( ai_output ) == DRAW:
					diff_new = DRAW - ai_output
					diff_old = DRAW - pos_draw["out"]
					pos_draw["col"] = x if diff_new < diff_old else pos_draw["col"]
				elif round( ai_output ) == LOSS:
					diff_new = LOSS - ai_output
					diff_old = LOSS - pos_loss["out"]
					pos_loss["col"] = x if diff_new < diff_old else pos_loss["col"]

			# Select best possible result
			if pos_win["col"] > 0:
				use_pos = pos_win["col"]
			elif pos_draw["col"] > 0:
				use_pos = pos_draw["col"]
			elif pos_loss["col"] > 0:
				use_pos = pos_loss["col"]
			# This shouldn't be possible
			else:
				print "-- The AI has no idea what to do and stares mindlessly at a cloud outside the window."
				print "-- The cloud looks like a rabbit riding a pony."
				print "-- You win by forfeit."
				break

			print "AI places stone in column " + str( use_pos ) + "."
			y = self.current_height[use_pos]
			self.board[use_pos][y] = STONE_AI
			self.current_height[use_pos] += 1

			self.print_board( self.board )

			winner = self.check_win()
			if winner == STONE_HUMAN:
				print "You won!"
				break
			elif winner == STONE_AI:
				print "The AI won!"
				break

			# Draw
			if self.check_board_full():
				print "No more free fields. It's a draw!"
				break

		print "Game ended."


	def print_board( self, board ):
		""" Print the current game board. """

		for y in reversed( range( FIELD_HEIGHT ) ):
			sys.stdout.write( " | " )
			for x in range( FIELD_WIDTH ):
				field = ' '
				if board[x][y] == STONE_HUMAN:
					field = 'x'
				elif board[x][y] == STONE_AI:
					field = 'o'
				sys.stdout.write( field + " | " )
			print ''
		sys.stdout.write( ' ' )
		print '¯' * ( FIELD_WIDTH * 4 + 1 )



if __name__ == "__main__":
	# Small test
	g = Game( None )
	print g.board
	g.print_board( g.board )
	print "Well, nothing crashed …"