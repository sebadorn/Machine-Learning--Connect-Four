#!/usr/bin/python
# -*- encoding: utf-8 -*-

VERBOSE = True

DATA_LIMIT = 400 # Limit data to use for training (67557 in total)
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
MLP_ES_DIFF = 0.01 # Error difference in early stopping
MLP_ETA = 0.3
MLP_EXPORT_FILE = "export_mlp.txt"
MLP_HIDDEN_NODES = 20
MLP_ITER = 100
MLP_MOMENTUM = 0.6
MLP_OUTTYPE = "linear"