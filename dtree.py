#!/usr/bin/python
# -*- coding: utf-8 -*-

from global_vars import *
import numpy as ny


class DTree:
	""" Decision Tree.
	Code based on chapter 6 of 'Machine Learning: An Algorithmic Perspective' by Stephen Marsland.
	(http://seat.massey.ac.nz/personal/s.r.marsland/MLBook.html)
	"""


	def __init__( self ):
		""" Constructor. """


	def classify( self, tree, datapoint ):
		"""

		tree      --
		datapoint --
		"""

		# Reached a leaf
		if type( tree ) == type( "string "):
			return tree
		# Not a leaf, proceed
		else:
			a = tree.keys()[0]
			for i in range( len( self.feature_names ) ):
				if self.feature_names[i] == a:
					break

			try:
				t = tree[a][datapoint[i]]
				return self.classify( t, datapoint )
			except:
				return None


	def classify_all( self, tree, data ):
		"""

		tree --
		data --
		"""

		results = []
		for i in range( len( data ) ):
			results.append( self.classify( tree, data[i] ) )

		return results


	def make_tree( self, data, classes, feature_names, max_level = -1, level = 0 ):
		""" Construct the tree.

		data          --
		classes       --
		feature_names --
		max_level     --
		level         --
		"""

		data_amount = len( data )
		feature_amount = len( data[0] )

		try: self.feature_names
		except: self.feature_names = feature_names

		# Get existing classes
		new_classes = []
		for some_class in classes:
			if new_classes.count( some_class ) == 0:
				new_classes.append( some_class )

		# Compute the default class
		frequency = ny.zeros( len( new_classes ) )
		entropy_total, gini_total, index = 0, 0, 0

		for some_class in new_classes:
			frequency[index] = classes.count( some_class )
			entropy_total += self.calc_entropy( float( frequency[index] ) / data_amount )
			gini_total += ( float( frequency[index] ) / data_amount ) ** 2
			index += 1

		gini_total = 1 - gini_total
		default_class = classes[ny.argmax( frequency )]

		# Empty branch
		if data_amount == 0 or feature_amount == 0 or ( max_level >= 0 and level > max_level ):
			return default
		# There is only one class left
		elif classes.count( classes[0] ) == data_amount:
			return classes[0]
		# We have to go deeper
		else:
			# Choose best feature
			gain = ny.zeros( feature_amount )
			ggain = ny.zeros( feature_amount )

			for feature in range( feature_amount ):
				g, gg = self.calc_info_gain( data, classes, feature )
				gain[feature] = entropy_total - g
				ggain[feature] = gini_total - gg

			best_feature = ny.argmax( gain )
			tree = { feature_names[best_feature]:{} }

			# Possible values of <best_feature>
			values = []
			for datapoint in data:
				if values.count( datapoint[best_feature] ) == 0:
					values.append( datapoint[best_feature] )

			# Find datapoints to each value of the feature
			for value in values:
				new_data, new_classes, index = [], [], 0
				for datapoint[best_feature] == value:
					if best_feature == 0:
						new_datapoint = datapoint[1:]
						names_new = feature_names[1:]
					elif best_feature == feature_amount:
						new_datapoint = datapoint[:-1]
						names_new = feature_names[:-1]
					else:
						new_datapoint = datapoint[:best_feature]
						new_datapoint.extend( datapoint[best_feature + 1:] )
						names_new = feature_names[:best_feature]
						names_new.extend( feature_names[best_feature + 1:] )
					new_data.append( new_datapoint )
					new_classes.append( classes[index] )
				index += 1

			# Build the next part of the tree
			subtree = self.make_tree( new_data, new_classes, new_names, max_level, level + 1 )

			tree[feature_names[best_feature]][value] = subtree

		return tree


	def calc_entropy( self, p ):
		""" 

		p --
		"""

		return -p * ny.log2( p ) if p != 0 else 0


	def calc_info_gain( self, data, classes, feature ):
		""" 

		data    --
		classes --
		feature --
		"""

		gain, ggain, data_amount = 0, 0, len( data )

		# Possible values the feature can take
		values = [], possible_values = 0
		for datapoint in data:
			if values.count( datapoint[feature] ) == 0:
				values.append( datapoint[feature] )
				possible_values += 1

		feature_counts = ny.zeros( possible_values )
		entropy = ny.zeros( possible_values )
		gini = ny.zeros( possible_values )
		value_index = 0

		for value in values:
			data_index, new_classes = 0, []
			for datapoint in data:
				if datapoint[feature] == value:
					feature_counts[value_index] += 1
					new_classes.append( classes[data_index] )
				data_index += 1

			class_values = []
			for some_class in new_classes:
				if class_values.count( some_class ) == 0:
					class_values.append( some_class )

			class_counts = ny.zeros( len( class_values ) )
			class_index = 0
			for class_value in class_values:
				for some_class in new_classes:
					if some_class == class_value:
						class_counts[class_index] += 1
					class_index += 1

			for class_index in range( len( class_values ) ):
				entropy[value_index] += self.calc_entropy( float( class_counts[class_index] ) / ny.sum( class_counts ) )
				gini[value_index] += ( float( class_counts[class_index] ) / ny.sum( class_counts ) ) ** 2

			gain += float( feature_counts[value_index] ) / data_amount * entropy[value_index]
			ggain += float( feature_counts[value_index] ) / data_amount * gini[value_index]
			value_index += 1

		return gain, 1 - ggain



if __name__ == "__main__":
	# Test the neuronal networks with a simple problem: XOR.
	inputs  = [[0,0], [0,1], [1,0], [1,1]]
	targets = [[0], [1], [1], [0]]

	print "Testing DTree with XOR:"

	my_dtree = DTree()

	out = []
	out_targets = [[0], [0], [1], [1], [1], [0]]

	correct = 0
	for i in range( len( out ) ):
		if out[i][0] == out_targets[i][0]: correct += 1
		else: print "  False: %d == %d" % ( out[i][0], out_targets[i][0] )

	print "Correct: %d/%d" % ( correct, len( out ) )

	# export_file = "export_dtree_xor.txt"
	# my_dtree.export( export_file )
	# print "Weight layers exported to %s." % export_file
	# my_dtree.import_weights( export_file )
	# print "Weight layers imported from %s." % export_file