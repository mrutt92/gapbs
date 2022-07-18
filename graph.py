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

