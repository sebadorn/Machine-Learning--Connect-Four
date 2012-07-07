#!/usr/bin/python
# -*- coding: utf-8 -*-

from global_vars import *
import numpy as ny


class DTree:
	"""
	Decision Tree.
	Code based on the code to the article "Building Decision Trees in Python - O'Reilly Media".
	(http://onlamp.com/pub/a/python/2006/02/09/ai_decision_trees.html)
	"""


	def __init__( self, data, attributes, target_attr ):
		"""
		Constructor.
		"""

		self.data = data[:]
		self.attributes = attributes[:]
		self.target_attr = target_attr
		self.tree = None


	def train( self ):
		"""
		Build the decision tree.
		"""

		self.tree = self._make_tree( self.data, self.attributes, self.target_attr )


	def _make_tree( self, data, attributes, target_attr ):
		"""
		Build the decision tree.
		"""

		data = data[:]
		values = [record[self.target_attr] for record in data]
		default = self._majority_value( data, target_attr )

		if not data or len( attributes ) - 1 <= 0:
			return default
		elif values.count( values[0] ) == len( values ):
			return values[0]
		else:
			best = self._choose_attribute( data, attributes, target_attr )
			tree = { best: {} }

			for value in self._get_values( data, best ):
				subtree = self._make_tree(
					self._get_examples( data, best, value ),
					[attr for attr in attributes if attr != best],
					target_attr
				)
				tree[best][value] = subtree

		return tree


	def _majority_value( self, data, target_attr ):
		"""
		Creates a list of all values in the target attribute for each record
		in the data, and return the value that appears the most frequently.
		"""

		lst = [record[target_attr] for record in data]
		highest_freq = 0
		most_freq = None
		unique_lst = list( set( lst ) )

		for val in unique_lst:
			if lst.count( val ) > highest_freq:
				most_freq = val
				highest_freq = lst.count( val )

		return most_freq


	def _choose_attribute( self, data, attributes, target_attr ):
		"""
		Cycles through all the attributes and returns the attribute
		with the highest information gain (or lowest entropy).
		"""

		data = data[:]
		best_gain = 0.0
		best_attr = None

		for attr in attributes:
			gain = self._gain( data, attr, target_attr )
			if gain >= best_gain and attr != target_attr:
				best_gain = gain
				best_attr = attr

		return best_attr


	def _get_values( self, data, attr ):
		"""
		Creates a list of values in the given attribute for
		each recod in the data.
		"""

		data = data[:]
		lst = [record[attr] for record in data]
		return list( set( lst ) )


	def _get_examples( self, data, attr, value ):
		"""
		Returns a list of all the records in <data> with
		the value of <attr> matching the given value.
		"""

		data = data[:]
		lst = []

		if not data:
			return lst
		else:
			record = data.pop()
			if record[attr] == value:
				lst.append( record )
				lst.extend( self._get_examples( data, attr, value ) )
				return lst
			else:
				lst.extend( self._get_examples( data, attr, value ) )
				return lst


	# def classify( self, data, tree = None ):
	# 	"""
	# 	Returns a list of classifications for each of the records in the data.
	# 	"""

	#	if tree is None:
	#		tree = self.tree

	# 	data = data[:]
	# 	classification = []

	# 	for record in data:
	# 		classification.append( self.use( record, tree ) )

	# 	return classification


	def _entropy( self, data, target_attr ):
		"""
		Calculate the entropy of the given data for the target attribute.
		"""

		val_freq = {}
		data_entropy = 0.0

		for record in data:
			key = record[target_attr]
			if val_freq.has_key( key ):
				val_freq[key] += 1.0
			else:
				val_freq[key] = 1.0

		for freq in val_freq.values():
			data_entropy += -freq / len( data ) * ny.log2( freq / len( data ) )

		return data_entropy


	def _gain( self, data, attr, target_attr ):
		"""
		Calculate the information gain (reduction in entropy) that would
		result by splitting the data on the given attribute.
		"""

		val_freq = {}
		subset_entropy = 0.0

		for record in data:
			key = record[attr]
			if val_freq.has_key( key ):
				val_freq[key] += 1.0
			else:
				val_freq[key] = 1.0

		for val in val_freq.keys():
			val_prob = val_freq[val] / ny.sum( val_freq.values() )
			data_subset = [record for record in data if record[attr] == val]
			subset_entropy += val_prob * self._entropy( data_subset, target_attr )

		return self._entropy( data, target_attr ) - subset_entropy


	def use( self, record, tree = None ):
		"""
		Return a classification for the given record.
		"""

		if tree is None:
			tree = self.tree

		if type( tree ) == type( "string" ):
			return tree
		else:
			attr = tree.keys()[0]
			t = tree[attr][record[attr]]
			return self.use( record, t )



if __name__ == "__main__":
	# Test the neuronal networks with a simple problem: XOR.
	attributes = ["a", "b", "r"]
	inputs = [[0,0,"no"], [0,1,"yes"], [1,0,"yes"], [1,1,"no"]]

	data = []
	for value in inputs:
		zipped = zip( attributes, [datum for datum in value] )
		data.append( dict( zipped ) )

	print "Testing DTree with XOR:"
	my_dtree = DTree( data, attributes, attributes[len( attributes ) - 1] )
	my_dtree.train()

	out = [
		my_dtree.use( {"a":0,"b":0} ), my_dtree.use( {"a":0,"b":1} ),
		my_dtree.use( {"a":1,"b":0} ), my_dtree.use( {"a":1,"b":1} ),
		my_dtree.use( {"a":1,"b":1} ), my_dtree.use( {"a":0,"b":1} )
	]
	targets = ["no", "yes", "yes", "no", "no", "yes"]

	correct = 0
	for i in range( len( targets ) ):
		if out[i] == targets[i]: correct += 1
		else: print "  False: %s == %s" % ( out[i], targets[i] )
	print "Correct: %d/%d" % ( correct, len( targets ) )

	# export_file = "export_mlp_xor.txt"
	# my_mlp.export( export_file )
	# print "Weight layers exported to %s." % export_file
	# my_mlp.import_weights( export_file )
	# print "Weight layers imported from %s." % export_file