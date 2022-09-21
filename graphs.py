def graph(gtype, gscale, gavgdegree):
    ofile.write("graphs += $(call graph,{},{},{}).al\n".format(gtype,gscale,gavgdegree))
    ofile.write("graphs += $(call graph,{},{},{}).el\n".format(gtype,gscale,gavgdegree))
    ofile.write("graphs += $(call graph,{},{},{}).mtx\n".format(gtype,gscale,gavgdegree))

gtypes = ['u','g', 'z']
#gscales = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
gscales = [7, 10, 16, 20]
gavgdegrees = [1, 2, 3, 4, 5, 6, 7, 8]

with open('graphs.mk','w') as ofile:
    for gtype in gtypes:
        for gscale in gscales:
            for gavgdegree in gavgdegrees:
                graph(gtype, gscale, gavgdegree)
