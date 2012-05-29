#!/usr/bin/python
# -*- coding: utf-8 -*-

import mlp

def print_bold( text ):
	print chr( 0x1b ) + "[1m" + text + chr( 0x1b ) + "[0m"


# Test the neuronal networks with a simple problem: XOR.

inputs  = [[0,0], [0,1], [1,0], [1,1]]
targets = [[0],   [1],   [1],   [0]]


if __name__ == "__main__":
	print " ----- ----- ----- -----"
	print_bold( " Testing MLP with XOR:" )
	my_mlp = mlp.MLP( inputs, targets, hidden_nodes = 2 )
	my_mlp.train( eta = 0.2, iterations = 1000, outtype = "logistic" )
	out = [
		round( my_mlp.use( [0,0] ) ), round( my_mlp.use( [0,1] ) ),
		round( my_mlp.use( [1,0] ) ), round( my_mlp.use( [1,1] ) )
	]
	target = [0,1,1,0]
	correct = 0
	for i in range( 4 ):
		if out[i] == target[i]: correct += 1
		else: print "     False: %d == %d" % ( out[i], target[i] )
	print " Correct: %d/4" % correct
	print " ----- ----- ----- -----"