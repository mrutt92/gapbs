from scipy.sparse import csr_matrix
from scipy.io import mmwrite, mmread

def graph_from_edge_list(el, transpose = False):
    """
    Returns a (V, E, neighbors) triplet
    """
    # initialize neighbors
    neighbors = {}
    V = 0
    E = 0
    # read in the graph
    with open(el,'r') as ifile:
        for line in ifile:
            src, dst = map(int,line.split(' '))
            mjr = src if not transpose else dst
            mnr = dst if not transpose else src
            if mjr not in neighbors:
                neighbors[mjr]  = [mnr]
            else:
                neighbors[mjr] += [mnr]
            # update E and V
            E += 1
            V = max(V, mjr, mnr)

        # sort each row
        for v in neighbors:
            neighbors[v].sort()

    # set V
    V=V+1
    return (V, E, neighbors)


def graph_from_mtx(mtx):
    # initalize neighbors
    neighbors = {}
    V = 0
    E = 0
    # read in mm
    csr = mmread(mtx)
    (sources, destinations) = csr.nonzero()
    (rows, columns) = csr.shape
    # set rows
    V = rows
    E = len(sources)
    for (src,dst) in zip(*csr.nonzero()):
        if src not in neighbors:
            neighbors[src]  = [dst]
        else:
            neighbors[src] += [dst]

    # sort each row
    for v in neighbors:
        neighbors[v].sort()

    return (V, E, neighbors)
