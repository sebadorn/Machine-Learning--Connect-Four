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

		self.nodes_in = len( inputs[0] )
		self.nodes_out = len( targets[0] )
		self.data_amount = len( inputs )

		self.weights = ny.random.rand( self.nodes_in + 1, self.nodes_out ) * 0.1 - 0.05


	def train( self, inputs, targets, eta, iterations ):
		""" Train the perceptron.

		inputs     --
		targets    --
		eta        --
		iterations --
		"""

		# Add bias node
		ones = -ny.ones( ( self.data_amount, 1 ) )
		inputs = ny.concatenate( ( inputs, ones ), axis = 1 )

		change = range( self.data_amount )
		for n in range( iterations ):
			outputs = self._forward( inputs )
			trans_in = ny.transpose( inputs )

			self.weights += eta * ny.dot( trans_in, targets - outputs )

			ny.random.shuffle( change )
			inputs = inputs[change,:]
			targets = targets[change,:]


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
		Returns the classification by the perceptron. Which either 1 or 0.
		"""

		return self._forward( inputs )