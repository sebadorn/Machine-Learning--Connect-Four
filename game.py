#!/usr/bin/python
# -*- encoding: utf-8 -*-

from global_vars import *
import sys, random, numpy as ny
import mlp


class Game:
	""" Play a game of Connect Four. """

	UP = 1
	RIGHT = 2
	DIAGONAL_RIGHT = 3
	DIAGONAL_LEFT = 4


	def __init__( self, ai ):
		self.ai = ai
		self._init_field()


	def _init_field( self ):
		""" Init play field. """

		self.board = ny.array( [[STONE_BLANK] * FIELD_HEIGHT] * FIELD_WIDTH )
		self.current_height = [0] * FIELD_WIDTH


	def input_validate( self, x ):
		""" Validates the chosen column x. """

		# Try to cast to a number
		try:
			x = int( x )
		except:
			return False

		# Outside of game board width.
		if x < 1 or x > FIELD_WIDTH:
			return False

		# Column is full.
		if self.current_height[x - 1] >= FIELD_HEIGHT:
			return False

		return True


	def _find_forced_move( self, x, y, direction ):
		""" Check if the next move is a forced one and where to place the stone.
		This function assumes, that for the given start position (x, y) three connected
		stones have already been found. Now it checks, if it is a dangerous situation.

		x         -- Start position (x coordinate) for the check.
		y         -- Start position (y coordinate) for the check.
		direction -- UP, RIGHT, DIAGONAL_LEFT or DIAGONAL_RIGHT.

		Returns the position where to place the stone or -1 if not necessary.
		"""
		# TODO: Doesn't recognize gaps between stones. |x|x| |x|

		force_x = -1
		stone = self.board[x][y]

		if direction == self.UP:
			if y + 3 < FIELD_HEIGHT and self.board[x][y + 3] == STONE_BLANK:
				force_x = x

		if direction == self.RIGHT:
			if x + 3 < FIELD_WIDTH and self.board[x + 3][y] == STONE_BLANK:
				force_x = x + 3
			elif x - 1 >= 0 and self.board[x - 1][y] == STONE_BLANK:
				force_x = x - 1

		if direction == self.DIAGONAL_RIGHT:
			if x + 1 < FIELD_WIDTH and y + 1 < FIELD_HEIGHT and self.board[x + 1][y + 1] == STONE_BLANK:
				if self.board[x + 1][y] != STONE_BLANK:
					force_x = x + 1
			elif x - 1 >= 0 and y - 1 >= 0 and self.board[x - 1][y - 1] == STONE_BLANK:
				if y - 2 < 0 or self.board[x - 1][y - 2] != STONE_BLANK:
					force_x = x - 1

		if direction == self.DIAGONAL_LEFT:
			if x + 1 < FIELD_WIDTH and y - 1 >= 0 and self.board[x + 1][y - 1] == STONE_BLANK:
				if y - 2 < 0 or self.board[x + 1][y - 2] != STONE_BLANK:
					force_x = x + 1
			elif x - 1 >= 0 and y + 1 < FIELD_HEIGHT and self.board[x - 1][y + 1] == STONE_BLANK:
				if self.board[x - 1][y] != STONE_BLANK:
					force_x = x - 1

		return force_x


	def check_win( self ):
		""" Check the game board if someone has won.

		Returns the stone value of the winner and the position for a forced move
		(opponent has already three stones connected).
		"""

		forced_move = -1
		for x in range( FIELD_WIDTH ):
			for y in range( FIELD_HEIGHT ):
				stone = self.board[x][y]
				# We only care about players, not blank fields
				if stone == STONE_BLANK:
					count = 0; continue

				# Look up
				count = 0
				for i in range( 1, CONNECT ):
					if y + i >= FIELD_HEIGHT:
						break
					# C-c-c-combo breaker!
					if stone != self.board[x][y + i]:
						break
					count += 1
				# All stones connected: Winner found!
				if count + 1 == CONNECT:
					return stone, forced_move
				# One stone away from winning, next move of opponent is forced
				if count + 1 == CONNECT - 1:
					tmp_fm = self._find_forced_move( x, y, self.UP )
					forced_move = tmp_fm if tmp_fm >= 0 else forced_move

				# Look right
				count = 0
				for i in range( 1, CONNECT ):
					if x + i >= FIELD_WIDTH:
						break
					if stone != self.board[x + i][y]:
						break
					count += 1
				if count + 1 == CONNECT:
					return stone, forced_move
				if count + 1 == CONNECT - 1:
					tmp_fm = self._find_forced_move( x, y, self.RIGHT )
					forced_move = tmp_fm if tmp_fm >= 0 else forced_move

				# Look diagonal right
				count = 0
				for i in range( 1, CONNECT ):
					if x + i >= FIELD_WIDTH or y + i >= FIELD_HEIGHT:
						break
					if stone != self.board[x + i][y + i]:
						break
					count += 1
				if count + 1 == CONNECT:
					return stone, forced_move
				if count + 1 == CONNECT - 1:
					tmp_fm = self._find_forced_move( x, y, self.DIAGONAL_RIGHT )
					forced_move = tmp_fm if tmp_fm >= 0 else forced_move

				# Look diagonal left
				count = 0
				for i in range( 1, CONNECT ):
					if x - i < 0 or y + i >= FIELD_HEIGHT:
						break
					if stone != self.board[x - i][y + i]:
						break
					count += 1
				if count + 1 == CONNECT:
					return stone, forced_move
				if count + 1 == CONNECT - 1:
					tmp_fm = self._find_forced_move( x, y, self.DIAGONAL_LEFT )
					forced_move = tmp_fm if tmp_fm >= 0 else forced_move

		return STONE_BLANK, forced_move


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
			if not self.input_validate( x ):
				print "No valid field position!"
				continue
			x = int( x ) - 1

			# Place human stone
			y = self.current_height[x]
			self.current_height[x] += 1
			self.board[x][y] = STONE_HUMAN

			self.print_board( self.board )

			winner, forced_move = self.check_win()
			if winner == STONE_HUMAN:
				print "You won!"
				break
			elif winner == STONE_AI:
				print "The AI won!"
				break

			# Place AI stone
			# ("opp" as in "opponent")
			opp_win = { "col": -1, "diff": 100.0 }
			opp_draw = { "col": -1, "diff": 100.0 }
			opp_loss = { "col": -1, "diff": 100.0 }

			# Forced move, don't ask the AI
			if forced_move > -1 and forced_move < FIELD_WIDTH:
				print "forced_move = %d" % forced_move
				use_pos = forced_move
			# Let the AI decide
			else:
				for x in range( FIELD_WIDTH ):
					# Cell (y) in this column (x) we are currently testing
					y = self.current_height[x]
					if y >= FIELD_HEIGHT:
						continue

					# Don't change the real game board
					board_copy = self.board.copy()
					board_copy[x][y] = STONE_AI

					# Array format for the AI: 7x6 -> 1x42
					ai_board_format = []
					for i in range( FIELD_WIDTH ):
						ai_board_format.extend( board_copy[i] )

					# Get the possible outcome
					ai_output = self.ai.use( ai_board_format )[0][0]
					print x, ai_output

					# Difference between targets and output
					diff_loss = LOSS - ai_output
					diff_win = WIN - ai_output
					diff_draw = DRAW - ai_output

					if diff_loss < 0.0: diff_loss *= -1
					if diff_win < 0.0: diff_win *= -1
					if diff_draw < 0.0: diff_draw *= -1

					# Close to (opponents) LOSS
					if diff_loss <= diff_draw and diff_loss <= diff_win:
						if diff_loss < opp_loss["diff"]:
							opp_loss["col"] = x
							opp_loss["diff"] = diff_loss

					# Close to DRAW
					elif diff_draw <= diff_loss and diff_draw <= diff_win:
						if diff_draw < opp_draw["diff"]:
							opp_draw["col"] = x
							opp_draw["diff"] = diff_draw

					# Close to (opponents) WIN
					else:
						if diff_win < opp_win["diff"]:
							opp_win["col"] = x
							opp_win["diff"] = diff_win


				# Select best possible result
				print opp_loss, opp_draw, opp_win

				# We want the opponent to loose
				if opp_loss["col"] >= 0:
					use_pos = opp_loss["col"]

				# If that is not possible, at least go for a draw
				elif opp_draw["col"] >= 0:
					use_pos = opp_draw["col"]

				# Ugh, fine, if there is no other choice
				elif opp_win["col"] >= 0:
					use_pos = opp_win["col"]

				# This shouldn't happen
				else:
					print "-- The AI has no idea what to do and stares mindlessly at a cloud outside the window."
					print "-- The cloud looks like a rabbit riding a pony."
					print "-- You win by forfeit."
					break

			print "AI places stone in column " + str( use_pos + 1 ) + "."
			y = self.current_height[use_pos]
			self.board[use_pos][y] = STONE_AI
			self.current_height[use_pos] += 1

			self.print_board( self.board )

			winner, forced_move = self.check_win()
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