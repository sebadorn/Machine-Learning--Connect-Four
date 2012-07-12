#!/usr/bin/python
# -*- encoding: utf-8 -*-

from global_vars import *
import sys, random, numpy as ny
import mlp, rbf, dtree


class Game:
	""" Play a game of Connect Four. """

	FLAG_MLP = 1
	FLAG_RBF = 2
	FLAG_DTREE = 3


	def __init__( self, ai ):
		"""
		Constructor.

		ai -- Trained instance of game AI.
		"""

		self.ai = ai
		if isinstance( ai, mlp.MLP ):
			self.ai_flag = self.FLAG_MLP
		elif isinstance( ai, rbf.RBF ):
			self.ai_flag = self.FLAG_RBF
		elif isinstance( ai, dtree.DTree ):
			self.ai_flag = self.FLAG_DTREE

		self.count_ai_moves = 0
		self.last_move_human = 0

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
		"""
		Compares the value of the found stone with the existing stone types.
		Sets a stop flag if it is not possible anymore for either the human or the AI
		to connect enough stones.

		Returns a tuple in the form: ( position of a blank field, #ai, #human, flag_to_stop ).
		"""

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

		if x + CONNECT <= FIELD_WIDTH and y + CONNECT <= FIELD_HEIGHT:
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
		"""
		Check if it is possible to place a stone in the given field.

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
		"""
		Check if the next move is a forced one and where to place the stone.
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
		"""
		Check the game board if someone has won.

		Returns the stone value of the winner or the value
		of a blank stone if there is no winner yet.
		"""

		for x in range( FIELD_WIDTH ):
			for y in range( FIELD_HEIGHT ):
				# We only care about players, not blank fields
				if self.board[x][y] == STONE_BLANK:
					continue

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
		""" Returns true if there are no more free fields, false otherwise. """

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
			self._place_stone( x, STONE_HUMAN )
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


			forced_move = self._find_forced_move()

			# Forced move, don't ask the AI
			if forced_move > -1:
				if VERBOSE: print "forced_move = %d" % forced_move
				use_pos = forced_move
			else:
				use_pos = self._ask_ai()
				if use_pos < 0: break

			print "AI places stone in column " + str( use_pos + 1 ) + "."

			self._place_stone( use_pos, STONE_AI )
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


	def _place_stone( self, col, stone ):
		""" Place a stone in a column. """

		row = self.current_height[col]
		self.board[col][row] = stone
		self.current_height[col] += 1

		if stone == STONE_AI:
			self.count_ai_moves += 1
		elif stone == STONE_HUMAN:
			self.last_move_human = col


	def _ask_ai( self ):
		"""
		Ask the AI to choose a column.
		Returns the index of the column to use or -1 if something went wrong.
		"""

		# Place AI stone
		# ("opp" as in "opponent")
		opp_win = { "col": -1, "diff": 100.0 }
		opp_draw = { "col": -1, "diff": 100.0 }
		opp_loss = { "col": -1, "diff": 100.0 }

		# Shuffle order columns are presented to the AI.
		# If more than one column could be chosen as next move, it won't
		# be the same for every game with a little randomness like this.
		columns = range( FIELD_WIDTH )
		ny.random.shuffle( columns )
		for x in columns:
			# Cell (y) in this column (x) we are currently testing
			y = self.current_height[x]
			if y >= FIELD_HEIGHT:
				continue

			# The MLP AI has a bad habit to mimik the human player if he/she
			# chooses the column 3, 4 or 5 as first two moves. Which basically
			# means the AI can only loose. Stop the AI from doing that!
			if self.count_ai_moves == 0 and x == self.last_move_human:
				continue

			# Don't change the real game board
			board_copy = self.board.copy()
			board_copy[x][y] = STONE_AI

			# Array format for the AI: 7x6 -> 1x42
			ai_board_format = []
			for i in range( FIELD_WIDTH ):
				ai_board_format.extend( board_copy[i] )

			# Get the possible outcome
			# MLP
			if self.ai_flag == self.FLAG_MLP:
				ai_output = self.ai.use( ai_board_format )[0][0]

				# Difference between targets and output
				diff_loss = LOSS - ai_output
				diff_win = WIN - ai_output
				diff_draw = DRAW - ai_output
				if diff_loss < 0.0: diff_loss *= -1
				if diff_win < 0.0: diff_win *= -1
				if diff_draw < 0.0: diff_draw *= -1

				if VERBOSE: print "Col: %d  Out: %f" % ( x, ai_output )

				# Close to (opponents) LOSS
				if diff_loss <= diff_draw:
					if diff_loss < opp_loss["diff"]:
						opp_loss["col"] = x
						opp_loss["diff"] = diff_loss

				# Close to DRAW
				else: # diff_draw <= diff_loss
					if diff_draw < opp_draw["diff"]:
						opp_draw["col"] = x
						opp_draw["diff"] = diff_draw

				# Don't even check for the (opponents) WIN case.
				# Rather take the least worse DRAW column.


			# RBF
			elif self.ai_flag == self.FLAG_RBF:
				win, draw, loss = self.ai.use( ai_board_format )[0]

				if VERBOSE: print "Col: %d  Out: %d/%d/%d" % ( x, win, draw, loss )

				if loss == 1: opp_loss["col"] = x
				elif draw == 1: opp_draw["col"] = x
				elif win == 1: opp_win["col"] = x


			# DTree
			elif self.ai_flag == self.FLAG_DTREE:
				for i in range( len( ai_board_format ) ):
					if ai_board_format[i] == STONE_BLANK:
						ai_board_format[i] = "b"
					elif ai_board_format[i] == STONE_HUMAN:
						ai_board_format[i] = "x"
					elif ai_board_format[i] == STONE_AI:
						ai_board_format[i] = "o"
				ai_board_format = dict( zip( DATA_ATTRIBUTES[:-1], ai_board_format ) )

				ai_output = self.ai.use( ai_board_format )

				if ai_output == "loss":
					opp_loss["col"] = x
				elif ai_output == "draw":
					opp_draw["col"] = x
				# Prefer an unknown outcome over yourself losing.
				elif ai_output == "unknown" and opp_draw["col"] == -1:
					opp_draw["col"] = x
				elif ai_output == "win":
					opp_win["col"] = x

				if VERBOSE: print "Col: %d  Outcome: %s" % ( x, ai_output )


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
			return -1

		return use_pos


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