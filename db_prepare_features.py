"""
Use db_prepared.cv and extract relevant features to compare two drivers.
The features will describe an OBJECT

1. L1 (distance)
2. proportion

Each time handle a specific race data, and make couples from that race alone.
Do this for each and every race
"""

def prepare_L1():
    objects = {}

