# See LICENSE.txt for license details.

CXX_FLAGS += -std=c++11 -O3 -Wall
PAR_FLAG = -fopenmp

ifneq (,$(findstring icpc,$(CXX)))
	PAR_FLAG = -openmp
endif

ifneq (,$(findstring sunCC,$(CXX)))
	CXX_FLAGS = -std=c++11 -xO3 -m64 -xtarget=native
	PAR_FLAG = -xopenmp
endif

ifneq ($(SERIAL), 1)
	CXX_FLAGS += $(PAR_FLAG)
endif

KERNELS = bc bfs cc cc_sv pr pr_spmv sssp tc
SUITE = $(KERNELS) converter

.PHONY: all
all: $(SUITE)

% : src/%.cc src/*.h
	$(CXX) $(CXX_FLAGS) $< -o $@

# Testing
include test/test.mk

# Benchmark Automation
include benchmark/bench.mk


graph = $(1)$(2)k$(3)
graph-type   = $(findstring u,$(1))$(findstring g,$(1))
graph-scale  = $(firstword $(subst k, ,$(subst u, ,$(subst g, ,$(1)))))
graph-degree = $(lastword $(subst k, ,$(1)))

include graphs.mk

$(filter %.al,$(graphs)): %.al: converter
	$(eval type=$(call graph-type,$*))
	$(eval scale=$(call graph-scale,$*))
	$(eval degree=$(call graph-degree,$*))
	./converter -l $@ -$(type) $(scale) -k $(degree)

$(filter %.el,$(graphs)): %.el: converter
	$(eval type=$(call graph-type,$*))
	$(eval scale=$(call graph-scale,$*))
	$(eval degree=$(call graph-degree,$*))
	./converter -e $@ -$(type) $(scale) -k $(degree)

$(filter %.mtx,$(graphs)): %.mtx: %.el
	$(eval scale=$(call graph-scale,$*))
	python3 el2mtx.py $< $(scale) $*

graphs: $(graphs)

.PHONY: clean
clean:
	rm -f $(SUITE) test/out/*
	rm -f $(graphs)
