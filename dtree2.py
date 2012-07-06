#!/usr/bin/python
# -*- coding: utf-8 -*-

from global_vars import *
import numpy as ny


class DTree2:
	""" Decision Tree.
	Code based on the article "Building Decision Trees in Python - O'Reilly Media".
	(http://onlamp.com/pub/a/python/2006/02/09/ai_decision_trees.html)
	"""


	def __init__( self ):
		""" Constructor. """


	def make_tree( self, data, attributes, target_attr, fitness_function ):
		""" Build the decision tree.

		data             --
		attributes       --
		target_attr      --
		fitness_function --
		"""

		data = data[:]
		values = [record[target_attr] for record in data]
		default = self.majority_value( data, target_attr )

		if not data or len( attributes ) - 1 <= 0:
			return default
		elif values.count( values[0] ) == len( values ):
			return values[0]
		else:
			best = self.choose_attribute( data, attributes, target_attr, fitness_function )
			tree = { best: {} }

			for value in self.get_values( data, best ):
				subtree = self.make_tree(
					self.get_examples( data, best, value ),
					[attr for attr in attributes if attr != best],
					target_attr,
					fitness_function
				)
				tree[best][value] = subtree

		return tree



	def majority_value( self, data, target_attr ):
		""" """

		return most_frequent( [record[target_attr] for record in data] )


	def choose_attribute( self, data, attributes, target_attr, fitness_function ):
		""" """


	def get_values( self, data, best ):
		""" """