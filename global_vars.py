#!/usr/bin/python
# -*- encoding: utf-8 -*-


# Limit data to use for training (67557 in total)
DATA_LIMIT = 10000

# Game board
FIELD_WIDTH = 7
FIELD_HEIGHT = 6
CONNECT = 4

# Stones
STONE_BLANK = 1.0
STONE_HUMAN = 2.0
STONE_AI = 3.0

# Results
WIN = 0.333
DRAW = 0.667
LOSS = 1.0

# Config MLP
MLP_BETA = 1.0
MLP_ES_DIFF = 0.01 # Error difference in early stopping
MLP_ETA = 0.3
MLP_EXPORT_FILE = "export_mlp.txt"
MLP_HIDDEN_NODES = 20
MLP_ITER = 100
MLP_MOMENTUM = 0.9
MLP_OUTTYPE = "linear"