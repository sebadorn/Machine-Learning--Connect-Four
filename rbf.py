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

	def __init__( self, inputs, targets, rbfs_amount, sigma = 0, use_kmeans = False, normalize = False ):
		""" Constructor.

		inputs      -- Input data for training.
		targets     -- Target data to inputs.
		rbfs_amount -- Amount of RBF nodes.
		sigma       -- 
		use_kmeans  -- Use k-means to initialise weights. Default: False
		normalize   -- Default: False
		"""

		self.inputs = ny.array( inputs )
		self.targets = ny.array( targets )
		self.rbfs_amount = rbfs_amount

		self.nodes_in = len( self.inputs[0] )
		self.nodes_out = len( self.targets[0] )
		self.data_amount = len( self.inputs )

		self.use_kmeans = use_kmeans
		self.normalize = normalize

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

		self.hidden = self._hidden_nodes_activation( self.inputs, self.hidden )
		self.perceptron.train( self.hidden[:,:-1], self.targets, eta, iterations )


	def _hidden_nodes_activation( self, inputs, hidden ):
		""" Use input data on the RBFs with the activation function.

		inputs -- Input data to use on the activation function.
		hidden -- 
		"""

		ones_input = ny.ones( ( 1, self.nodes_in ) )
		sigma_square = 2 * self.sigma ** 2

		for i in range( self.rbfs_amount ):
			tmp = inputs - ones_input * self.weights[:,i]
			hidden[:,i] = ny.exp( -ny.sum( tmp ** 2, axis = 1 ) / sigma_square )

		if self.normalize:
			ones_hidden = ny.ones( ( 1, len( hidden ) ) )
			hidden[:,:-1] /= ny.transpose( ones_hidden * hidden[:,:-1].sum( axis = 1 ) )

		return hidden


	def _forward( self, inputs ):
		""" Forward the network.

		inputs -- Input data to forward through the network.
		"""

		# Throw input data on the RBF
		hidden = ny.zeros( ( len( inputs ), self.rbfs_amount + 1 ) )
		hidden = self._hidden_nodes_activation( inputs, hidden )
		# Bias node
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

	my_rbf = RBF( inputs, targets, sigma = 1, rbfs_amount = 4 )
	my_rbf.train( eta = 0.2, iterations = 400 )

	out = [
		my_rbf.use( [0,0] ), my_rbf.use( [1,1] ),
		my_rbf.use( [0,1] ), my_rbf.use( [1,0] ),
		my_rbf.use( [0,1] ), my_rbf.use( [1,1] )
	]
	out_targets = [[0], [0], [1], [1], [1], [0]]

	correct = 0
	for i in range( len( out ) ):
		if out[i] == out_targets[i][0]: correct += 1
		else: print "  False: %d == %d" % ( out[i], out_targets[i][0] )

	print "Correct: %d/%d" % ( correct, len( out ) )

	# export_file = "export_rbf_xor.txt"
	# my_rbf.export( export_file )
	# print "Weight layers exported to %s." % export_file
	# my_rbf.import_weights( export_file )
	# print "Weight layers imported from %s." % export_file
