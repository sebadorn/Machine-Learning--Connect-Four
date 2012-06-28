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


	def _count_stones( self, column, row, stone, blank, ai, human ):
		""" Compares the value of the found stone with the existing stone types.
		Sets a stop flag if it is not possible anymore for either the human or the AI
		to connect enough stones.

		Returns a tuple in the form: ( position of a blank field, #ai, #human, flag_to_stop ). """

		flag_stop = False

		if stone == STONE_BLANK:
			# No danger/chance if there is more than one blank field in range
			if blank != -1: flag_stop = True
			# Save blank field. This is a candidate to place the stone.
			else: blank = { "col": column, "row": row }
		elif stone == STONE_AI:
			# If there has been at least one human stone already,
			# it is not possible for AI stones to have a connection of three and a blank field available.
			if human > 0: flag_stop = True
			else: ai += 1
		elif stone == STONE_HUMAN:
			# Same here, vice versa.
			if ai > 0: flag_stop = True
			else: human += 1

		return ( blank, ai, human, flag_stop )


	def _count_stones_up( self, x, y ):
		""" From position (x,y) count the types of the next stones upwards. """

		blank, ai, human = -1, 0, 0

		if y + CONNECT <= FIELD_HEIGHT:
			for i in range( CONNECT ):
				col, row = x, y + i
				stone = self.board[col][row]
				blank, ai, human, flag_stop = self._count_stones( col, row, stone, blank, ai, human )
				if flag_stop: break

		return ( blank, ai, human )


	def _count_stones_right( self, x, y ):
		""" From position (x,y) count the types of the next stones to the right. """

		blank, ai, human = -1, 0, 0

		if x + CONNECT <= FIELD_WIDTH:
			for i in range( CONNECT ):
				col, row = x + i, y
				stone = self.board[col][row]
				blank, ai, human, flag_stop = self._count_stones( col, row, stone, blank, ai, human )
				if flag_stop: break

		return ( blank, ai, human )


	def _count_stones_rightup( self, x, y ):
		""" From position (x,y) count the types of the next stones diagonal right up. """

		blank, ai, human = -1, 0, 0

		if x + CONNECT <= FIELD_WIDTH and y + CONNECT < FIELD_HEIGHT:
			for i in range( CONNECT ):
				col, row = x + i, y + i
				stone = self.board[col][row]
				blank, ai, human, flag_stop = self._count_stones( col, row, stone, blank, ai, human )
				if flag_stop: break

		return ( blank, ai, human )


	def _count_stones_rightdown( self, x, y ):
		""" From position (x,y) count the types of the next stones diagonal right down. """

		blank, ai, human = -1, 0, 0

		if x + CONNECT <= FIELD_WIDTH and y - CONNECT + 1 >= 0:
			for i in range( CONNECT ):
				col, row = x + i, y - i
				stone = self.board[col][row]
				blank, ai, human, flag_stop = self._count_stones( col, row, stone, blank, ai, human )
				if flag_stop: break

		return ( blank, ai, human )


	def _check_proposed_col( self, pos ):
		""" Check if it is possible to place a stone in the given field.

		Returns True if possible, False otherwise.
		"""

		if pos == -1:
			return False

		if pos["col"] >= 0 and pos["col"] < FIELD_WIDTH:
			# Check if it is possible to place the stone at the needed height
			if pos["row"] == 0 or self.board[pos["col"]][pos["row"] - 1] != STONE_BLANK:
				return True

		return False


	def _find_forced_move( self ):
		""" Check if the next move is a forced one and where to place the stone.
		A forced move occurs if the human player or the AI could win the game with the next move.

		Returns the position where to place the stone or -1 if not necessary.
		"""

		force_x = -1

		for x in range( FIELD_WIDTH ):
			for y in range( FIELD_HEIGHT ):

				# Check: UP
				blank, ai, human = self._count_stones_up( x, y )
				# Evaluate: UP
				if blank != -1:
					# If there is a chance to win: Do it!
					if ai == 3: return blank["col"]
					# Remember dangerous situation for now.
					# Maybe there will be a chance to win somewhere else!
					elif human == 3:
						if VERBOSE: print "[human] could win UP with %d." % blank["col"]
						force_x = blank["col"]

				# Check: RIGHT
				blank, ai, human = self._count_stones_right( x, y )
				# Evaluate: RIGHT
				if self._check_proposed_col( blank ):
					if ai == 3: return blank["col"]
					elif human == 3:
						if VERBOSE: print "[human] could win RIGHT with %d." % blank["col"]
						force_x = blank["col"]

				# Check: DIAGONAL RIGHT UP
				blank, ai, human = self._count_stones_rightup( x, y )
				# Evaluate: DIAGONAL RIGHT UP
				if self._check_proposed_col( blank ):
					if ai == 3: return blank["col"]
					elif human == 3:
						if VERBOSE: print "[human] could win DIAGONAL RIGHT UP with %d." % blank["col"]
						force_x = blank["col"]

				# Check: DIAGONAL RIGHT DOWN
				blank, ai, human = self._count_stones_rightdown( x, y )
				# Evaluate: DIAGONAL RIGHT DOWN
				if self._check_proposed_col( blank ):
					if ai == 3: return blank["col"]
					elif human == 3:
						if VERBOSE: print "[human] could win DIAGONAL RIGHT DOWN with %d." % blank["col"]
						force_x = blank["col"]

		return force_x


	def check_win( self ):
		""" Check the game board if someone has won.

		Returns the stone value of the winner or
		the value of a blank stone if there is no winner yet.
		"""

		for x in range( FIELD_WIDTH ):
			for y in range( FIELD_HEIGHT ):
				# We only care about players, not blank fields
				if self.board[x][y] == STONE_BLANK:
					count = 0; continue

				# Check: UP
				blank, ai, human = self._count_stones_up( x, y )
				if ai == CONNECT: return STONE_AI
				elif human == CONNECT: return STONE_HUMAN

				# Check: RIGHT
				blank, ai, human = self._count_stones_right( x, y )
				if ai == CONNECT: return STONE_AI
				elif human == CONNECT: return STONE_HUMAN

				# Check: DIAGONAL RIGHT UP
				blank, ai, human = self._count_stones_rightup( x, y )
				if ai == CONNECT: return STONE_AI
				elif human == CONNECT: return STONE_HUMAN

				# Check: DIAGONAL RIGHT DOWN
				blank, ai, human = self._count_stones_rightdown( x, y )
				if ai == CONNECT: return STONE_AI
				elif human == CONNECT: return STONE_HUMAN

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
			if not self.input_validate( x ):
				print "No valid field position!"
				continue
			x = int( x ) - 1

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
				print "The AI won!"
				break

			forced_move = self._find_forced_move()

			# Place AI stone
			# ("opp" as in "opponent")
			opp_win = { "col": -1, "diff": 100.0 }
			opp_draw = { "col": -1, "diff": 100.0 }
			opp_loss = { "col": -1, "diff": 100.0 }

			# Forced move, don't ask the AI
			if forced_move > -1:
				if VERBOSE: print "forced_move = %d" % forced_move
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
				if VERBOSE: print opp_loss, opp_draw, opp_win

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