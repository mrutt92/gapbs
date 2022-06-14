import sys
import numpy as np
import pandas
import matplotlib.pyplot as pp
import seaborn as sns

edge_list = sys.argv[1]
data = pandas.read_csv(edge_list, names=['src','dst'], delim_whitespace=True)

#out_degrees = pandas.pivot_table(data, values=['src'], aggfunc='count')
out_degrees = data.groupby('src').count()
in_degrees  = data.groupby('dst').count()

nodes = data['src'].nunique()
edges = data['src'].count()

mean_degree   = int(out_degrees['dst'].mean())
median_degree = int(out_degrees['dst'].median())

print("from graph {:10}: {:13} : {:9d}, {:23} : {:9d}".format(
    edge_list
    ,"nodes"
    ,nodes
    ,"edges"
    ,edges
))

srcs_with_mean_degree = out_degrees[out_degrees['dst']==mean_degree]
src_with_mean_degree  = srcs_with_mean_degree.sample(1, axis=0, random_state=0).index[0]
print('from graph {:10}: {:13} : {:9d}, {:23} : {:9d}'.format(
    edge_list
    ,"mean degree"
    ,mean_degree
    ,"node with mean degree"
    ,src_with_mean_degree
))

srcs_with_median_degree = out_degrees[out_degrees['dst']==median_degree]
src_with_median_degree  = srcs_with_median_degree.sample(1, axis=0, random_state=0).index[0]
print('from graph {:10}: {:13} : {:9d}, {:23} : {:9d}'.format(
    edge_list
    ,"median degree"
    ,median_degree
    ,"node with median degree"
    ,src_with_median_degree
))

ax = sns.ecdfplot(out_degrees)
# set yticks 
yticks = np.arange(0.0, 1.1, 0.1)
ax.set_yticks(yticks)

# set xticks
odmax = int(out_degrees.max())
if edge_list.startswith('g'):
    ax.set_xscale('log')
else:
    xticks = np.arange(0, odmax+1, odmax/20)
    ax.set_xticks(xticks)

ax.grid(True, linestyle='-')
pp.show()
