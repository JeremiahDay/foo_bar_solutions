from collections import defaultdict
from copy import copy

def solution(l):
    '''
    Finds the number of "lucky triples" in list l

    Per docs, incoming list is already in analysis order. Given this,
    each edge in the digraph points from an element to the appropriate
    whole-number products _later in the list_. Resulting digraph is 
    acyclical and in topological (analysis) order
    '''
    codes = HashArray(l)
    g = Digraph(len(codes))
    for count, v in enumerate(codes.array, 1): # slow, len(l)**2 / 2 ops
        for w in codes[count::1]:
            if (w // v > 1) and (w % v == 0):
                g.add_edge(v, w)
    count = 0
    for v in codes.array:
        count += g.triple_count(v)
    
    return v

class Digraph(object):
    def __init__(self, V):
        self._V = V  # number of vertices
        self._adj = [list() for _ in range(self._V)] # list of lists

    def add_edge(self, v, w):
        self._adj[v].append(w)

    @property
    def adj(self):
        return self._adj
    
    def triple_count(self, s):
        # counts all triples that start from a given vertex 's'
        # uses non-recursive dfs to perform count
        count = 0
        for w in self.adj[s]:
            count += len(self.adj[w])
        return count

class HashArray(object):
    def __init__(self, items):
        #  Takes as input list of ints, returns a dict with ints as keys,
        #  array indices as values
        self._V = len(items)  # number of values
        self._array = copy(items)  # try to avoid clobbering...
        self._d = defaultdict(list)
        for count, i in enumerate(self._array):
            self._d[i].append(count)

    def __len__(self):
        return len(self._array)

    def __getitem__(self, index):
        # returns value at index; index may be an int or a slice object
        return self._array[index]

    @property
    def array(self):
        return self._array

    def find(self, key):
        # returns a list of all indices with array[index] equal to key
        return self._d[key]

if __name__ == '__main__':
    s = solution([1, 2, 3, 4, 5, 6])
    print(s)