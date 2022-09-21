import sys
from statistics import median
import argparse as argp
from graph import *
import pandas as pd

parser = argp.ArgumentParser()
parser.add_argument('mtx0')
parser.add_argument('mtx1')

arguments = parser.parse_args()
mtx0 = arguments.mtx0
mtx1 = arguments.mtx1


V_0i, E_0i, neighbors_0i = graph_from_mtx(mtx0)
V_1i, E_1i, neighbors_1i = graph_from_mtx(mtx1)

V_o = V_0i
E_o = 0
neighbors_o = {}

# stats on the second input matrix
stats_i1 = {
    'ROW_i1'  : [i for i in range(V_1i)],
    'NNZ_i1'  : [len(neighbors_1i[i]) if i in neighbors_1i else 0 for i in range(V_1i)],
    'READ_i1' : [0 for i in range(V_1i)],
}


# stats on the output matrix
stats_o = {
    'ROW_o'  : [],
    'NNZ_0i' : [],
    'NNZ_1i' : [],
    'NNZ_MAX_1i' : [],
    'NNZ_MIN_1i' : [],
    'NNZ_MED_1i' : [],
    'NNZ_o'  : [],
    'FMUL'   : [],
    'FADD'   : [],
}

# row-wise product
for i in range(V_0i):
    row_stats = {
        'ROW_o'  : i,
        'NNZ_0i' : 0,
        'NNZ_1i' : 0,
        'NNZ_MAX_1i' : 0,
        'NNZ_MIN_1i' : 0,
        'NNZ_MED_1i' : 0,
        'NNZ_o'  : 0,
        'FMUL'   : 0,
        'FADD'   : 0,
    }

    # skip if no non-zeros
    if i in neighbors_0i:
        row_o = {}
        nnz_1i = []

        for k in neighbors_0i[i]:
            # update the stats for second input matrix
            stats_i1['READ_i1'][k]+=1

            # skip if no non-zeros
            row_stats['NNZ_0i'] += 1
            if k not in neighbors_1i:
                nnz_1i.append(0)
                continue

            nnz_1i.append(len(neighbors_1i[k]))

            # count non-zeros
            for j in neighbors_1i[k]:
                row_stats['FMUL'] += 1
                if j in row_o:
                    row_stats['FADD'] += 1
                    row_o[j] += 1
                else:
                    row_o[j] = 1

        # set the row
        neighbors_o[i] = [j for j in row_o]
        neighbors_o[i].sort()

        # update the stats
        row_stats['NNZ_o'] = len(neighbors_o[i])
        row_stats['NNZ_1i'] = sum(nnz_1i)
        row_stats['NNZ_MAX_1i'] = max(nnz_1i)
        row_stats['NNZ_MIN_1i'] = min(nnz_1i)
        row_stats['NNZ_MED_1i'] = median(nnz_1i)

    # update the stats
    for k in stats_o:
        stats_o[k].append(row_stats[k])

pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)

data = pd.DataFrame(stats_o)
data.to_csv(mtx0 + '_x_' + mtx1 + '.stats_o.csv')
#print(data)

data = pd.DataFrame(stats_i1)
data.to_csv(mtx0 + '_x_' + mtx1 + '.stats_i1.csv')
#print(data)
