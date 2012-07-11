#!/usr/bin/python
# -*- coding: utf-8 -*-

from global_vars import *
import os, sys, numpy as ny
import mlp, rbf, dtree, game


# Explanation for the trainings data:
# Every line contains equal amounts of x and o stones.
# The win/loss/draw indicates the outcome for the next
# player, if both follow a perfect plan.


def my_converter( x ):
	""" Converter for Numpys loadtxt function.
	Replace the strings with float values.
	"""

	if x == 'x': return STONE_HUMAN
	elif x == 'o': return STONE_AI
	elif x == 'b': return STONE_BLANK
	elif x == "win": return WIN
	elif x == "loss": return LOSS
	elif x == "draw": return DRAW


def normalize( data ):
	""" Normalize given data. """

	sys.stdout.write( " Normalizing data ..." )
	sys.stdout.flush()

	data -= data.mean( axis = 0 )
	imax = ny.concatenate(
		(
			data.max( axis = 0 ) * ny.ones( ( 1, len( data[0] ) ) ),
			data.min( axis = 0 ) * ny.ones( ( 1, len( data[0] ) ) )
		), axis = 0 ).max( axis = 0 )
	data /= imax

	return data


def import_traindata( file_in ):
	""" Import the file with training data for the AI. """

	sys.stdout.write( "Importing training data ..." )
	sys.stdout.flush()

	# Assign converters for each attribute.
	# A dict where the key is the index for each attribute.
	# The value for each key is the same function to replace the string with a float.
	convs = dict( zip( range( DATA_NUM_ATTR + 1 ) , [my_converter] * DATA_NUM_ATTR ) )
	connectfour = ny.loadtxt( file_in, delimiter = ',', converters = convs )

	cf_original = []
	f = open( file_in, "r" )
	for line in f:
		cf_original.append( line.split( ',' ) )

	# Split in data and targets
	data = connectfour[:,:DATA_NUM_ATTR - 1]
	targets = connectfour[:,DATA_NUM_ATTR - 1:DATA_NUM_ATTR]

	if DATA_NORMALIZE:
		data = normalize( data )

	sys.stdout.write( " Done.\n\n" )

	return data, targets, cf_original


def print_bold( text ):
	""" Print bold text to the console. """

	print chr( 0x1b ) + "[1m" + text + chr( 0x1b ) + "[0m"


def print_help():
	""" Display the help. """

	print "Available commands:"
	print_bold( "    General" )
	print "    exit     - Leave the program."
	print "    help     - Display this help."
	print
	print_bold( "    Handling the AI" )
	print "    select *  - Select the AI type to use: MLP, RBF"
	print "    train     - Train the previously selected AI."
	print "    play      - Play Connect Four."
	print "    export    - Export brain of AI."
	print "    export_js - Export brain of AI as Javascript."
	print "    import    - Import brain of AI."
	print


def select_ai( cl, data, targets, original_import ):
	"""
	Select an AI. Create in instance of the needed class and return it.
	"""
	ai = None

	# MLP
	if cl == "MLP":
		ai = mlp.MLP(
			data, targets,
			hidden_nodes = MLP_HIDDEN_NODES, beta = MLP_BETA, momentum = MLP_MOMENTUM
		)
		print "MLP created."

	# RBF
	elif cl == "RBF":
		# Adjust target format for RBF: [win, draw, loss]
		targets_rbf = ny.zeros( ( len( targets ), 3 ) )
		for i in range( len( targets ) ):
			win = 1 if targets[i] == WIN else 0
			draw = 1 if targets[i] == DRAW else 0
			loss = 1 if targets[i] == LOSS else 0
			targets_rbf[i] = [win, draw, loss]

		ai = rbf.RBF(
			data, targets_rbf,
			sigma = RBF_SIGMA, rbfs_amount = RBF_NODES, use_kmeans = RBF_KMEANS, normalize = RBF_NORMALIZE
		)

		print "RBF created."

	# DTree
	elif cl == "DTree":
		data = []
		for value in original_import:
			zipped = zip( DATA_ATTRIBUTES, [datum for datum in value] )
			data.append( dict( zipped ) )
		ai = dtree.DTree( data, DATA_ATTRIBUTES, DT_TARGET_ATTRIBUTE )

		print "DTree created."

	return ai


def train_ai( ai, valid, validtargets ):
	"""
	Train the previously selected AI.
	"""

	if not ai:
		print "Training not possible. You have to select an AI type first."
	else:
		# MLP
		if isinstance( ai, mlp.MLP ):
			ai.early_stopping(
				valid, validtargets,
				eta = MLP_ETA, iterations = MLP_ITER, outtype = MLP_OUTTYPE
			)

		# RBF
		elif isinstance( ai, rbf.RBF ):
			ai.train( eta = RBF_ETA, iterations = RBF_ITER )

		# DTree
		elif isinstance( ai, dtree.DTree ):
			ai.train()

		else:
			print "Training not possible. Unknown AI."

		print "Training completed."



if __name__ == "__main__":
	print "// Training an artificial intelligence to play Connect Four."
	print "// Author: Sebastian Dorn"
	print "// Type 'help' for more."
	print

	# Import data for training
	data, targets, original_import = import_traindata( FILE_DATA )

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

		if cl == "exit":
			break
		elif cl == "help":
			print_help()

		# Select an AI
		elif cl.startswith( "select " ):
			cl = cl.replace( "select ", "" )

			ai = select_ai( cl, data, targets, original_import )
			if ai is None:
				print "ERROR: Unknown AI."

		# Training
		elif cl == "train":
			train_ai( ai, valid, validtargets )

		# Start a game with the trained AI
		elif cl == "play":
			vg = game.Game( ai )
			vg.play()

		# Export the weights of the AI
		elif cl == "export":
			ai.export()
			print "Export completed."

		elif cl == "export_js":
			ai.export_js()
			print "Export completed."

		# Import weights into the AI
		elif cl == "import":
			ai.import_ai()
			print "Import completed."

		elif cl != "":
			print "Unknown command."