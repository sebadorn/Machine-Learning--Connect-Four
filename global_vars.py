#!/usr/bin/python
# -*- encoding: utf-8 -*-


# Limit data to use for training (67557 in total)
DATA_LIMIT = 1000

# Game board
FIELD_WIDTH = 7
FIELD_HEIGHT = 6
CONNECT = 4

# Stones
STONE_BLANK = 1.0
STONE_HUMAN = 2.0
STONE_AI = 3.0

# Results
WIN = 1.0
DRAW = 2.0
LOSS = 3.0

# Config
MLP_HIDDEN_NODES = 20
MLP_ETA = 0.6
MLP_ITER = 100
MLP_OUTTYPE = "linear"
MLP_ES_DIFF = 0.001 # Error difference in early stopping