#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import mlp


FILE_DATA = "connect-4.data"


def import_traindata( file ):
	""" Import the file with training data for the AI. """

	a_end = -1
	data = []
	targets = []
	f = open( file, 'r' )

	for line in f:
		attr = line.split( ',' )
		if a_end < 0:
			a_end = len( attr ) - 1

		data.append( attr[:-1] )
		targets.append( attr[a_end].replace( '\n', '' ) )

	f.close()
	return data, targets


def print_bold( text ):
	print chr( 0x1b ) + "[1m" + text + chr( 0x1b ) + "[0m"


def print_help():
	""" Display the help. """

	print "Available commands:"
	print_bold( "    General" )
	print "    exit           - Leave the program."
	print "    help           - Display this help."
	print
	print_bold( "    Handling the AI" )
	print "    import <*.vgw> - Imports file with model weights."
	print "    export <*.vgw> - Exports file with model weights."
	print



if __name__ == "__main__":
	print "// VG"
	print "// Training an artificial intelligence to play Connect Four."
	print "// Author: Sebastian Dorn"
	print "// Type 'help' for more."
	print

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
		elif cl == "import":
			import_traindata( FILE_DATA )
		else:
			print "Unknown command."