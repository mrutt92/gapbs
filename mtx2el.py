from scipy.sparse import csr_matrix
from scipy.io import mmwrite, mmread
import numpy as np
import pandas as pd
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('mtx', help='Matrix market file')
parser.add_argument('edge_list', help='Edge list output')

arguments = parser.parse_args()
matrix_market = arguments.mtx
edge_list = arguments.edge_list

print(matrix_market)
print(edge_list)

with open(edge_list, "w") as el_file:
    csr = mmread(matrix_market)
    (sources,destinations) = csr.nonzero()
    for (src,dst) in zip(*csr.nonzero()):
        el_file.write("%d %d\n" % (src,dst))


