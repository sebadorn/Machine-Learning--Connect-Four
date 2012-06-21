#!/usr/bin/python
# -*- coding: utf-8 -*-

from global_vars import *
import numpy as ny


class kmeans:
	""" k-Means
	Code based on chapter 4 of 'Machine Learning: An Algorithmic Perspective' by Stephen Marsland.
	(http://seat.massey.ac.nz/personal/s.r.marsland/MLBook.html)
	"""

	def __init__( self, k, data ):
		""" Constructor.

		k    -- Expected number of classes.
		data -- Input data to build clusters for.
		"""

		self.data = data
		self.data_amount = len( data )
		self.data_dim = len( data[0] )
		self.k = k


	def train( self, iter_limit = 10 ):
		""" Train.

		iter_limit -- Maximum number of iterations. Default: 10

		Returns the cluster centres.
		"""

		# Minimum and maximum for each feature.
		minima = self.data.min( axis = 0 )
		maxima = self.data.max( axis = 0 )

		# Centers
		self.centres = ny.random.rand( self.k, self.data_dim ) * ( maxima - minima ) + minima
		old_centres = ny.random.rand( self.k, self.data_dim ) * ( maxima - minima ) + minima

		count = 0
		while ny.sum( ny.sum( old_centres - self.centres ) ) != 0 and count < iter_limit:
			old_centres = self.centres.copy()
			count += 1

			cluster = self._forward( self.data )
			self._update( cluster )

		return self.centres


	def _forward( self ):
		""" Run forward.

		Returns the closest cluster.
		"""

		ones_data = ny.ones( ( 1, self.data_amount ) )

		# Distance between input data and current cluster centres.
		dist = ones_data * ny.sum( ( self.data - self.centres[0,:] ) ** 2, axis = 1 )
		for i in range( self.k - 1 ):
			dist = ny.append( dist, ones_data * ny.sum( ( self.data - self.centres[i + 1,:] ) ** 2, axis = 1 ), axis = 0 )

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
