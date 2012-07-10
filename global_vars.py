#!/usr/bin/python
# -*- encoding: utf-8 -*-

VERBOSE = True

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
MLP_EXPORT_FILE = "export_mlp.txt"
MLP_EXPORT_FILE_JS = "web/export_mlp.js"
MLP_HIDDEN_NODES = 40
MLP_ITER = 40
MLP_MOMENTUM = 0.7
MLP_OUTTYPE = "linear"

# Config RBF
RBF_ETA = 0.4
RBF_EXPORT_FILE = "export_rbf.txt"
RBF_EXPORT_FILE_JS = "web/export_rbf.js"
RBF_ITER = 100
RBF_KMEANS = True
RBF_NODES = 200
RBF_NORMALIZE = True
RBF_SIGMA = 0

# Config DTree
DT_EXPORT_FILE = "export_dtree.txt"
DT_EXPORT_FILE_JS = "web/export_dtree.js"
DT_TARGET_ATTRIBUTE = "outcome"