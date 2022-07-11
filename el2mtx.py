from scipy.sparse import csr_matrix
from scipy.io import mmwrite
import numpy as np
import pandas as pd
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('edge_list', help='Edge list file')
parser.add_argument('scale', type=int, help='Scale of matrix (exponential)')
parser.add_argument('mmfile_base', help='Matrix market file basename')

arguments = parser.parse_args()
edge_list = arguments.edge_list
scale = arguments.scale
matrix_market = arguments.mmfile_base

n = 2**scale

data = pd.read_csv(edge_list, names=['src','dst'], delim_whitespace=True)
rows = np.array(data['src'])
cols = np.array(data['dst'])
vals = np.random.rand(rows.size)
matrix = csr_matrix((vals, (rows,cols)), shape=(n,n))

mmwrite(matrix_market, matrix)
