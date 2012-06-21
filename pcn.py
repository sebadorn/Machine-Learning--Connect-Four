#!/usr/bin/python
# -*- coding: utf-8 -*-

from global_vars import *
import numpy as ny


class Perceptron:
	""" Perceptron
	Code based on chapter 4 of 'Machine Learning: An Algorithmic Perspective' by Stephen Marsland.
	(http://seat.massey.ac.nz/personal/s.r.marsland/MLBook.html)
	"""

	def __init__( self, inputs, targets ):
		""" Constructor.

		inputs  --
		targets --
		"""

		self.inputs = inputs
		self.targets = targets

		self.nodes_in = len( self.inputs[0] )
		self.nodes_out = len( self.targets[0] )
		self.data_amount = len( self.inputs )

		# Add bias node
		ones = -ny.ones( ( self.data_amount, 1 ) )
		self.inputs = ny.concatenate( ( self.inputs, ones ), axis = 1 )

		self.weights = ny.random.rand( self.nodes_in + 1, self.nodes_out ) * 0.1 - 0.05


	def train( self, eta, iterations ):
		""" Train the perceptron.

		eta        --
		iterations --
		"""

		change = range( self.data_amount )
		for n in range( iterations ):
			self.outputs = self._forward( self.inputs )

			trans_in = ny.transpose( self.inputs )
			self.weights += eta * ny.dot( trans_in, self.targets - self.outputs )

			ny.random.shuffle( change )
			self.inputs = self.inputs[change,:]
			self.targets = self.targets[change,:]


	def _forward( self, inputs ):
		""" Forward the network.

		inputs -- Input data to run forward.
		Returns the output of the activation function.
		"""

		outputs = ny.dot( inputs, self.weights )

		# Activation function
		return ny.where( outputs > 0, 1, 0 )


	def use( self, inputs ):
		""" Use the trained network. Which means running it forward.

		inputs -- Input data to use the trained perceptron on.
		Returns the classification by the perceptron.
		"""

		return self._forward( inputs )