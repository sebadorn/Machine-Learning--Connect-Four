#!/usr/bin/python
# -*- coding: utf-8 -*-

from global_vars import *
import numpy as ny
import pcn, kmeans


class RBF:
	""" Radial Basis Function Network
	Code based on chapter 4 of 'Machine Learning: An Algorithmic Perspective' by Stephen Marsland.
	(http://seat.massey.ac.nz/personal/s.r.marsland/MLBook.html)
	"""

	def __init__( self, inputs, targets, rbfs_amount, sigma = 0, use_kmeans = False, normalise = False ):
		""" Constructor.

		inputs      -- Input data for training.
		targets     -- Target data to inputs.
		rbfs_amount -- Amount of RBF nodes.
		sigma       -- 
		use_kmeans  -- Use k-means to initialise weights. Default: False
		normalise   -- Default: False
		"""

		self.inputs = ny.array( inputs )
		self.targets = ny.array( targets )
		self.rbfs_amount = rbfs_amount

		self.nodes_in = len( self.inputs[0] )
		self.nodes_out = len( self.targets[0] )
		self.data_amount = len( self.inputs )

		self.use_kmeans = use_kmeans
		self.normalise = normalise

		if self.use_kmeans:
			self.kmeans_net = kmeans.kmeans( self.rbfs_amount, self.inputs )

		self.hidden = ny.zeros( ( self.data_amount, self.rbfs_amount + 1 ) )

		if sigma == 0:
			d = ( self.inputs.max( axis = 0 ) - self.inputs.min( axis = 0 ) ).max()
			self.sigma = d / ny.sqrt( 2 * self.rbfs_amount )
		else:
			self.sigma = sigma

		self.perceptron = pcn.Perceptron( self.hidden[:,:-1], self.targets )

		self.weights = ny.zeros( ( self.nodes_in, self.rbfs_amount ) )


	def train( self, eta = 0.25, iterations = 100 ):
		""" Train the network.

		eta        -- 
		iterations -- 
		"""

		if self.use_kmeans == False:
			indices = range( self.data_amount )
			ny.random.shuffle( indices )
			for i in range( self.rbfs_amount ):
				self.weights[:,i] = self.inputs[indices[i],:]
		else:
			self.weights = ny.transpose( self.kmeans_net.train( self.inputs ) )

		for i in range( self.rbfs_amount ):
			tmp = self.inputs - ny.ones( ( 1, self.nodes_in ) ) * self.weights[:,i]
			sigma_square = 2 * self.sigma ** 2
			self.hidden[:,i] = ny.exp( -ny.sum( tmp ** 2, axis = 1 ) / sigma_square )

		if self.normalise:
			ones = ny.ones( ( 1, len( self.hidden ) ) )
			self.hidden[:,:-1] /= ny.transpose( ones * self.hidden[:,:-1].sum( axis = 1 ) )

		self.perceptron.train( eta, iterations )


	def _forward( self, inputs ):
		""" Forward the network.

		inputs --
		"""

		hidden = ny.zeros( ( len( inputs ), self.rbfs_amount + 1 ) )

		for i in range( self.rbfs_amount ):
			tmp = inputs - ny.ones( ( 1, self.nodes_in ) ) * self.weights[:,i]
			sigma_square = 2 * self.sigma ** 2
			hidden[:,i] = ny.exp( -ny.sum( tmp ** 2, axis = 1 ) / sigma_square )

		if self.normalise:
			ones = ny.ones( ( 1, len( hidden ) ) )
			hidden[:,:-1] /= ny.transpose( ones * hidden[:,:-1].sum( axis = 1 ) )

		# Bias ndoe
		hidden[:,-1] = -1

		# Run through perceptron and get activations
		outputs = self.perceptron.use( hidden )

		return outputs


	def use( self, inputs ):
		""" After training the network, now use it!

		inputs -- Input/test data.
		Returns the calculated output.
		"""

		return self._forward( inputs )



if __name__ == "__main__":
	# Test the neuronal networks with a simple problem: XOR.
	inputs  = [[0,0], [0,1], [1,0], [1,1]]
	targets = [[0], [1], [1], [0]]

	print "Testing RBF with XOR:"

	my_rbf = RBF( inputs, targets, rbfs_amount = 4 )
	my_rbf.train( eta = 0.2, iterations = 1000 )

	out = [
		my_rbf.use( [0,0] ), my_rbf.use( [0,1] ),
		my_rbf.use( [1,0] ), my_rbf.use( [1,1] )
	]

	correct = 0
	for i in range( 4 ):
		print out[i]
		#if out[i] == targets[i]: correct += 1
		#else: print "  False: %d == %d" % ( out[i], targets[i] )

	# print "Correct: %d/4" % correct

	# my_mlp.export()
	# print "Weight layers exported to %s." % MLP_EXPORT_FILE
	# my_mlp.import_weights()
	# print "Weight layers imported from %s." % MLP_EXPORT_FILE
