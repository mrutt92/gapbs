import sys
import argparse as argp
import pandas as pd

parser = argp.ArgumentParser()
parser.add_argument('edge_list')
parser.add_argument('--start', type=int, default=0)
parser.add_argument('--reverse', action='store_true')

arguments = parser.parse_args()
edge_list = arguments.edge_list
start = arguments.start

# initialize neighbors
neighbors = {}

V = 0
E = 0
# read in the graph
with open(edge_list,'r') as ifile:
    for line in ifile:
        src, dst = map(int,line.split(' '))
        mjr = src if not arguments.reverse else dst
        mnr = dst if not arguments.reverse else src
        if mjr not in neighbors:
            neighbors[mjr]  = [mnr]
        else:
            neighbors[mjr] += [mnr]
        # update E and V
        E += 1
        V = max(V, mjr, mnr)
# set V
V=V+1

# run bfs
# algorithm variables
frontier = set([start])
next_frontier = set()
visited  = set([start])
iteration = 0
direction = 'forward' if not arguments.reverse else 'reverse'

stats = {
    'heurstic_direction' : [],    
    'direction' : [],
    'iteration' : [],
    'traversed_edges'  : [],
    'updated_vertices' : [],
}

def sum_degree(frontier):
    d = 0
    for s in frontier:
        if not s in neighbors: continue
        d += len(neighbors[s])
    return d

if not arguments.reverse:
    # push direction bfs
    while frontier:
        # per-iteration stats
        traversed_edges = 0
        updated_vertices = 0
        heurstic_direction = 'reverse' if len(frontier)+sum_degree(frontier) > int(E/20) else 'forward'
        # for each src in the frontier
        for src in frontier:
            # skip if this vertex has no neighbors
            if src not in neighbors: continue
            # traverse each neighbor
            for dst in neighbors[src]:
                # check if we have visited
                traversed_edges += 1
                if dst not in visited:
                    updated_vertices += 1
                    visited.add(dst)
                    next_frontier.add(dst)

        # udpate the next frontier
        frontier = next_frontier
        next_frontier = set()
        # dump stats
        stats['heurstic_direction']+=[heurstic_direction]
        stats['iteration']+=[iteration]
        stats['traversed_edges']+=[traversed_edges]
        stats['updated_vertices']+=[updated_vertices]
        stats['direction']+=[direction]
        # update iteration
        iteration += 1
else:
    # pull direction bfs
    while frontier:
        # per-iteration stats
        traversed_edges = 0
        updated_vertices = 0
        heurstic_direction = 'reverse' if len(frontier)+sum_degree(frontier) > int(E/20) else 'forward'        
        # for each vertex in G        
        for dst in range(V):
            # skip if dst has already been visited
            if dst in visited: continue
            # skip if this vertex has no neighbors
            if dst not in neighbors: continue            
            # traverse in neighbors until we find one in the frontier
            for src in neighbors[dst]:
                traversed_edges += 1
                if src in frontier:
                    updated_vertices += 1
                    visited.add(dst)
                    next_frontier.add(dst)
                    break
        # update next frontier
        frontier = next_frontier
        next_frontier = set()
        # dump stats
        stats['heurstic_direction']+=[heurstic_direction]        
        stats['iteration']+=[iteration]
        stats['traversed_edges']+=[traversed_edges]
        stats['updated_vertices']+=[updated_vertices]
        stats['direction']+=[direction]
        # update iteration
        iteration += 1        

dataframe = pd.DataFrame(stats)
dataframe.to_csv(arguments.edge_list + '.{}.csv'.format(direction))
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
print(dataframe)
