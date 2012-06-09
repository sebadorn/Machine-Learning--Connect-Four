#!/usr/bin/python
# -*- coding: utf-8 -*-

from global_vars import *
import os, sys, numpy as ny
import mlp, game


# File name with training data
FILE_DATA = "connect-4.data"
# Number of attributes in each line
DATA_NUM_ATTR = 43


def my_converter( x ):
	""" Converter for Numpys loadtxt function.
	Replace the strings with float values.
	"""

	if x == 'x': return STONE_HUMAN
	elif x == 'o': return STONE_AI
	elif x == 'b': return STONE_BLANK
	elif x == "win": return LOSS # No, not a mistake
	elif x == "loss": return WIN # No, not a mistake
	elif x == "draw": return DRAW


def import_traindata( file_in ):
	""" Import the file with training data for the AI. """

	sys.stdout.write( "Importing training data ..." )
	sys.stdout.flush()

	# Assign converters for each attribute.
	# A dict where the key is the index for each attribute.
	# The value for each key is the same function to replace the string with a float.
	convs = dict( zip( range( DATA_NUM_ATTR + 1 ) , [my_converter] * DATA_NUM_ATTR ) )

	connectfour = ny.loadtxt( file_in, delimiter = ',', converters = convs )

	# Normalize
	connectfour -= connectfour.mean( axis = 0 )
	imax = ny.concatenate(
		(
			connectfour.max( axis = 0 ) * ny.ones( ( 1, 43 ) ),
			connectfour.min( axis = 0 ) * ny.ones( ( 1, 43 ) )
		), axis = 0 ).max( axis = 0 )
	connectfour /= imax

	# Split in data and targets
	data = connectfour[:,:DATA_NUM_ATTR - 1]
	targets = connectfour[:,DATA_NUM_ATTR - 1:DATA_NUM_ATTR]

	sys.stdout.write( " Done.\n\n" )

	return data, targets


def print_bold( text ):
	print chr( 0x1b ) + "[1m" + text + chr( 0x1b ) + "[0m"


def print_help():
	""" Display the help. """

	print "Available commands:"
	print_bold( "    General" )
	print "    exit     - Leave the program."
	print "    help     - Display this help."
	print
	print_bold( "    Handling the AI" )
	print "    select * - Select the AI type to use: MLP, RBF, DTree"
	print "    train    - Train the previously selected AI."
	print "    play     - Play Connect Four."
	print



if __name__ == "__main__":
	print "// Training an artificial intelligence to play Connect Four."
	print "// Author: Sebastian Dorn"
	print "// Type 'help' for more."
	print

	data, targets = import_traindata( FILE_DATA )

	shuffle = range( DATA_LIMIT )
	ny.random.shuffle( shuffle )
	data, targets = data[shuffle,:], targets[shuffle,:]
	valid, validtargets = data[:int( DATA_LIMIT / 3 )], targets[:int( DATA_LIMIT / 3 )]

	ai = False

	# Main loop
	while 1:
		# Get user input
		try:
			cl = raw_input( "> " )
		except EOFError: print; break
		except KeyboardInterrupt: print; break

		# Evaluate user input
		if cl == "exit":
			break
		elif cl == "help":
			print_help()

		elif cl.startswith( "select " ):
			cl = cl.replace( "select ", "" )
			if cl == "MLP":
				ai = mlp.MLP( data, targets, hidden_nodes = MLP_HIDDEN_NODES )
				print "MLP created."
			elif cl == "RBF":
				print "ERROR: RBF not yet implemented."
			elif cl == "DTree":
				print "ERROR: DTree not yet implemented."
			else:
				print "ERROR: Unknown AI type."

		elif cl == "train":
			if not ai:
				print "Training not possible. You have to select an AI type first."
			else:
				#ai.train()
				ai.early_stopping(
					valid, validtargets,
					eta = MLP_ETA, iterations = MLP_ITER, outtype = MLP_OUTTYPE
				)
				print "Training completed."

		elif cl == "play":
			vg = game.Game( ai )
			vg.play()

		elif cl != "":
			print "Unknown command."