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

	def __init__( self, inputs, targets, rbfs_amount,
			sigma = 0, use_kmeans = False, normalize = False ):
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
			self.kmeans_net = kmeans.kmeans( self.rbfs_amount )

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

		eta        -- Learning rate.
		iterations -- Number of rounds to the train the perceptron.
		"""

		if self.use_kmeans == False:
			indices = range( self.data_amount )
			ny.random.shuffle( indices )
			for i in range( self.rbfs_amount ):
				self.weights[:,i] = self.inputs[indices[i],:]
		else:
			self.weights = ny.transpose( self.kmeans_net.train( self.inputs ) )

		print "- Trained RBF nodes."

		self.hidden = self._hidden_nodes_activation( self.inputs, self.hidden )
		self.perceptron.train( self.hidden[:,:-1], self.targets, eta, iterations )

		print "- Trained perceptron."


	def _hidden_nodes_activation( self, inputs, hidden ):
		""" Use input data on the RBFs with the activation function.

		inputs -- Input data to use on the activation function.
		hidden -- Hidden layer of nodes.
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
		outputs = self.perceptron._forward( hidden )
		# outputs = self.perceptron.use( hidden )

		return outputs


	def use( self, inputs ):
		""" After training the network, now use it!

		inputs -- Input/test data.
		Returns the calculated output.
		"""

		return self._forward( inputs )


	def export( self, filename = RBF_EXPORT_FILE ):
		"""
		Export the weight layers of the RBF.
		"""

		layer_1, layer_2 = "", ""

		for line in self.weights:
			for ele in line:
				layer_1 += str( ele ) + " "
		layer_1 = layer_1.replace( '[', '' )
		layer_1 = layer_1.replace( ']', '' )
		layer_1 = layer_1.replace( '  ', ' ' )

		for line in self.perceptron.weights:
			for ele in line:
				layer_2 += str( ele ) + " "
		layer_2 = layer_2.replace( '[', '' )
		layer_2 = layer_2.replace( ']', '' )
		layer_2 = layer_2.replace( '  ', ' ' )

		f = open( filename, 'w' )
		f.write( "# Config:\n" )
		f.write( "# Eta: %f  Nodes: %d  Sigma: %f\n" % ( RBF_ETA, self.rbfs_amount, self.sigma ) )
		f.write(
			"# Iterations: %d  K-means: %d  Normalize: %d\n"
			% ( RBF_ITER, self.use_kmeans, self.normalize )
		)
		f.write( "\n# RBF\n" )
		f.write( layer_1 )
		f.write( "\n\n# Perceptron\n" )
		f.write( layer_2 )
		f.close()


	def export_js( self, filename = RBF_EXPORT_FILE_JS ):
		"""
		Export the weight layers of the RBF as Javascript.
		"""

		layer_1, layer_2 = "", ""

		count = 0
		for line in self.weights:
			for ele in line:
				count += 1
				if count == 1:
					layer_1 += "["
				if count == self.rbfs_amount:
					layer_1 += str( ele ) + "],\n"
					count = 0
				else:
					layer_1 += str( ele ) + ", "
		layer_1 = layer_1[:-2]

		count = 0
		for line in self.perceptron.weights:
			for ele in line:
				count += 1
				if count == 1:
					layer_2 += "["
				if count == self.nodes_out:
					layer_2 += str( ele ) + "],\n"
					count = 0
				else:
					layer_2 += str( ele ) + ", "
		layer_2 = layer_2[:-2]

		f = open( filename, 'w' )
		layers = [layer_1, layer_2]
		for i in range( len( layers ) ):
			f.write( "var RBF_weights_" + str( i + 1 ) + " = new Array(\n" )
			f.write( layers[i] )
			f.write( ");\n" )
		f.close()


	def import_ai( self, filename = RBF_EXPORT_FILE ):
		"""
		Imports weight layers from a file.
		"""

		f = open( filename, 'r' )

		values_layer1, values_layer2 = [], []

		import_layer = 0
		for line in f:
			line = line.strip()
			if len( line ) <= 1:
				continue
			elif line == "# RBF":
				import_layer = 1
				continue
			elif line == "# Perceptron":
				import_layer = 2
				continue
			elif line.startswith( '#' ):
				continue

			for value in line.split( ' ' ):
				if value == '':
					continue
				value = float( value.strip() )
				if import_layer == 1:
					values_layer1.append( value )
				elif import_layer == 2:
					values_layer2.append( value )

		i, j = 0, 0
		for v in values_layer1:
			if j >= self.rbfs_amount:
				j = 0
				i += 1
			self.weights[i][j] = v
			j += 1

		i, j = 0, 0
		for v in values_layer2:
			if j >= self.nodes_out:
				j = 0
				i += 1
			self.perceptron.weights[i][j] = v
			j += 1

		f.close()



if __name__ == "__main__":
	# Test the neuronal networks with a simple problem: XOR.
	inputs  = [[0,0], [0,1], [1,0], [1,1]]
	targets = [[0], [1], [1], [0]]

	print "Testing RBF with XOR:"

	my_rbf = RBF( inputs, targets, sigma = 1, rbfs_amount = 4, use_kmeans = True )
	my_rbf.train( eta = 0.2, iterations = 400 )

	out = [
		my_rbf.use( [0,0] ), my_rbf.use( [1,1] ),
		my_rbf.use( [0,1] ), my_rbf.use( [1,0] ),
		my_rbf.use( [0,1] ), my_rbf.use( [1,1] )
	]
	out_targets = [[0], [0], [1], [1], [1], [0]]

	correct = 0
	for i in range( len( out ) ):
		if out[i][0] == out_targets[i][0]: correct += 1
		else: print "  False: %d == %d" % ( out[i][0], out_targets[i][0] )

	print "Correct: %d/%d" % ( correct, len( out ) )

	export_file = "export_rbf_xor.txt"
	my_rbf.export( export_file )
	print "Weight layers exported to %s." % export_file
	my_rbf.import_ai( export_file )
	print "Weight layers imported from %s." % export_file

	print
	print "Testing imported RBF with XOR again:"

	out = [
		my_rbf.use( [1,0] ), my_rbf.use( [1,1] ),
		my_rbf.use( [0,1] ), my_rbf.use( [1,0] ),
		my_rbf.use( [0,1] ), my_rbf.use( [1,1] )
	]
	out_targets = [[1], [0], [1], [1], [1], [0]]

	correct = 0
	for i in range( len( out ) ):
		if out[i][0] == out_targets[i][0]: correct += 1
		else: print "  False: %d == %d" % ( out[i][0], out_targets[i][0] )

	print "Correct: %d/%d" % ( correct, len( out ) )
	my_rbf.export_js()