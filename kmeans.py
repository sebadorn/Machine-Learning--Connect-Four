#!/usr/bin/python
# -*- coding: utf-8 -*-

from global_vars import *
import numpy as ny


class kmeans:
	""" k-Means
	Code based on chapter 4 of 'Machine Learning: An Algorithmic Perspective' by Stephen Marsland.
	(http://seat.massey.ac.nz/personal/s.r.marsland/MLBook.html)
	"""

	def __init__( self, k ):
		""" Constructor.

		k    -- Expected number of classes.
		"""

		self.k = k


	def train( self, data, iter_limit = 10 ):
		""" Train.

		data       -- Input data to train with.
		iter_limit -- Maximum number of iterations. Default: 10

		Returns the cluster centres.
		"""

		self.data = data
		self.data_amount = len( data )
		self.data_dim = len( data[0] )

		# Minimum and maximum for each feature.
		minima = data.min( axis = 0 )
		maxima = data.max( axis = 0 )

		# Centers
		self.centres = ny.random.rand( self.k, self.data_dim ) * ( maxima - minima ) + minima
		centres_old = ny.random.rand( self.k, self.data_dim ) * ( maxima - minima ) + minima

		count = 0
		while ny.sum( ny.sum( centres_old - self.centres ) ) != 0 and count < iter_limit:
			centres_old = self.centres.copy()
			count += 1

			cluster = self._forward( data )
			self._update( cluster )

		return self.centres


	def _forward( self, data ):
		""" Run forward.

		Returns the closest cluster.
		"""

		ones_data = ny.ones( ( 1, self.data_amount ) )

		# Distance between input data and current cluster centres.
		dist = ones_data * ny.sum( ( data - self.centres[0,:] ) ** 2, axis = 1 )
		for i in range( self.k - 1 ):
			sum_square = ny.sum( ( data - self.centres[i + 1,:] ) ** 2, axis = 1 )
			dist = ny.append( dist, ones_data * sum_square, axis = 0 )

		# Find closest cluster
		cluster = dist.argmin( axis = 0 )
		cluster = ny.transpose( cluster * ones_data )

		return cluster


	def _update( self, cluster ):
		""" Update cluster centres.

		cluster -- The clusters.
		"""

		for i in range( self.k ):
			cluster_i = ny.where( cluster == i, 1, 0 )

			if ny.sum( cluster_i ) > 0:
				cluster_data_sum = ny.sum( self.data * cluster_i, axis = 0 )
				cluster_i_sum = ny.sum( cluster_i )
				self.centres[i,:] = cluster_data_sum / cluster_i_sum
