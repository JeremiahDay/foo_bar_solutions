from random import randint

def solution(l):
    '''
    Finds the number of "lucky triples" in list l

    Per docs, incoming list is already in analysis order. Given this,
    each edge in the digraph points from an element to the appropriate
    whole-number products _later in the list_. Resulting digraph is 
    acyclical and in topological (analysis) order

    Time complexity is O(n**2)
    '''
    codes = l
    g = Digraph(len(codes))
    for v in range(len(codes)):
        for w in range(v + 1, len(codes)):
            if (codes[w] >= codes[v]) and (codes[w] % codes[v] == 0):
                g.add_edge(v, w)
    count = 0
    for v in range(len(codes)):
        count += g.triple_count(v)
    
    return count

class Digraph(object):
    def __init__(self, V):
        self._V = V  # number of vertices
        self._adj = [list() for _ in range(self._V)] # list of lists

    def add_edge(self, v, w):
        self.adj[v].append(w)

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

if __name__ == '__main__':
    li = []
    for i in range (2000):
        li.append(randint(1, 200))
    s = solution(li)
    print(s)