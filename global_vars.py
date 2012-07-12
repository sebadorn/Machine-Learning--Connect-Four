#!/usr/bin/python
# -*- encoding: utf-8 -*-

VERBOSE = True

# File name with training data
FILE_DATA = "connect-4.data"
# Number of attributes in each line
DATA_NUM_ATTR = 43

DATA_LIMIT = 67557 # Limit data to use for training (67557 in total)
DATA_NORMALIZE = False

# Game board
FIELD_WIDTH = 7
FIELD_HEIGHT = 6
CONNECT = 4

# Stones
STONE_BLANK = 0.0
STONE_HUMAN = 1.0
STONE_AI = -1.0

# Results
WIN = 0.0
DRAW = 0.5
LOSS = 1.0

# Config MLP
MLP_BETA = 1.0
MLP_ES_DIFF = 1 # Error difference in early stopping
MLP_ES_MAX_ITER = 240
MLP_ETA = 0.35
MLP_EXPORT_FILE = "exports/export_mlp.txt"
MLP_EXPORT_FILE_JS = "web/export_mlp.js"
MLP_HIDDEN_NODES = 40
MLP_ITER = 40
MLP_MOMENTUM = 0.7
MLP_OUTTYPE = "linear"

# Config RBF
RBF_ETA = 0.4
RBF_EXPORT_FILE = "exports/export_rbf.txt"
RBF_EXPORT_FILE_JS = "web/export_rbf.js"
RBF_ITER = 40
RBF_KMEANS = True
RBF_NODES = 30
RBF_NORMALIZE = True
RBF_SIGMA = 0

# Config DTree
DT_EXPORT_FILE = "exports/export_dtree.txt"
DT_EXPORT_FILE_JS = "web/export_dtree.js"
DT_TARGET_ATTRIBUTE = "outcome"
DATA_ATTRIBUTES = [
	"a1","a2","a3","a4","a5","a6","b1","b2","b3","b4","b5","b6",
	"c1","c2","c3","c4","c5","c6","d1","d2","d3","d4","d5","d6",
	"e1","e2","e3","e4","e5","e6","f1","f2","f3","f4","f5","f6",
	"g1","g2","g3","g4","g5","g6", DT_TARGET_ATTRIBUTE
]