#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, numpy as ny
import mlp


# File name with training data
FILE_DATA = "connect-4.data"
# Number of attributes in each line
DATA_NUM_ATTR = 43
# Limit data to use for training
DATA_LIMIT = 10000


def my_converter( x ):
	""" Converter for Numpys loadtxt function.
	Replace the strings with float values.
	"""

	if x == 'x': return 1.0
	elif x == 'o': return 2.0
	elif x == 'b': return 0.0
	elif x == "win": return 1.0
	elif x == "loss": return 2.0
	elif x == "draw": return 3.0


def import_traindata( file_in, verbose = False ):
	""" Import the file with training data for the AI. """

	if verbose: sys.stdout.write( "Importing training data ..." ); sys.stdout.flush()

	# Assign converters for each attribute.
	# A dict where the key is the index for each attribute.
	# The value for each key is the same function to replace the string with a float.
	convs = dict( zip( range( DATA_NUM_ATTR + 1 ) , [my_converter] * DATA_NUM_ATTR ) )

	connectfour = ny.loadtxt( file_in, delimiter = ',', converters = convs )
	data = connectfour[:,:DATA_NUM_ATTR - 1]
	targets = connectfour[:,DATA_NUM_ATTR:DATA_NUM_ATTR - 1]

	if verbose: sys.stdout.write( " Done.\n\n" )

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
	print



if __name__ == "__main__":
	print "// Training an artificial intelligence to play Connect Four."
	print "// Author: Sebastian Dorn"
	print "// Type 'help' for more."
	print

	data, targets = import_traindata( FILE_DATA, verbose = True )

	shuffle = range( DATA_LIMIT )
	ny.random.shuffle( shuffle )
	data, targets = data[shuffle,:], targets[shuffle,:]

	ann = False

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
				ann = mlp.MLP( data, targets )
				print "MLP created."
			elif cl == "RBF":
				print "ERROR: RBF not yet implemented."
			elif cl == "DTree":
				print "ERROR: DTree not yet implemented."

		elif cl == "train":
			if not ann:
				print "Training not possible. You have to select an AI type first."
			else:
				ann.train()
				print "Training completed."

		else:
			print "Unknown command."