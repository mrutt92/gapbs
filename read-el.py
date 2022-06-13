import sys
import pandas
import matplotlib.pyplot as pp
import seaborn as sns

edge_list = sys.argv[1]
data = pandas.read_csv(edge_list, names=['src','dst'], delim_whitespace=True)

#out_degrees = pandas.pivot_table(data, values=['src'], aggfunc='count')
out_degrees = data.groupby('src').count()
in_degrees  = data.groupby('dst').count()

ax = sns.ecdfplot(out_degrees)
pp.show()
