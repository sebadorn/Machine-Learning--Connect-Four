#!/usr/bin/python
# -*- encoding: utf-8 -*-

import mlp


FIELD_WIDTH = 8
FIELD_HEIGHT = 6

STONE_BLANK = 0.0
STONE_HUMAN = 1.0
STONE_ANN = 2.0


class Game:
	""" Play a game of Connect Four. """


	def __init__( self, ann ):
		self.ann = ann
		self._init_field()


	def _init_field( self ):
		""" Init play field. """
		self.field = [[STONE_BLANK] * FIELD_WIDTH] * FIELD_HEIGHT
		self.current_height = [0] * FIELD_WIDTH


	def play( self ):
		while 1:
			try:
				x = raw_input( ">> Column: " )
			except EOFError: print; break
			except KeyboardInterrupt: print; break

			# Validate user input
			x = int( x )
			if x < 1 or x > 8:
				print "No valid field position!"
				continue

			# Place human stone
			y = self.current_height[x]
			self.current_height[x] += 1
			self.field[y][x] = STONE_HUMAN

			# Place ann stone
			ann_output = self.ann.use( self.field )
			print ann_output


		print "Game ended."



if __name__ == "__main__":
	# Small test
	g = Game( None )
	print "Well, nothing crashed …"