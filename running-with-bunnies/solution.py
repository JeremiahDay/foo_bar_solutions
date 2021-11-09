from collections import namedtuple, Counter, deque
from itertools import combinations, permutations

DirectedEdge = namedtuple('DirectedEdge', ['from_v', 'to_w', 'weight'])

def solution(times, time_limit):
    '''
    Discovers the optimal set of bunnies to rescue from a given corridor
    with weight matrix 'times' within a given 'time_limit'. Solution evaluates
    the problem as a minimum open hamiltonian walk where the times
    from the matrix are arc weights. As an open walk, arcs and vertices may
    be visited multiple times but the walk must begin at a certain vertex [0]
    and end at another distinct vertex [len(times) - 1].

    Since negative weights are allowed and negative cycles are permitted by
    the problem statement the solution can be divided into two: First,
    determine whether there are any negative cycles and return the full
    set of bunnies if so (since in a negative cycle the walker can generate
    as much time as necessary so all bunnies can be saved). Second, if
    there are no negative cycles search for shortest walk in the given matrix.
    Finding a shortest hamiltonian walk is equivalent to finding the shortest
    hamiltonian _cycle_ in the metric closure of the original matrix.

    Metric closure of a given graph G is defined as a second graph G', where
    all vertices are the same and arcs connect all vertices (a complete
    digraph) and the weight of each arc is the weight of the minimum path
    in G to/from the vertices at the arc ends.

    Finding a negative cycle in the matrix G and finding minimum paths
    between vertices in G are both solved using Bellman-Ford shortest paths
    algorithm. Once the metric closure weights have been found, weights
    for all paths from S -> [permutations of bunnies] -> T are calculated in
    lexical order and compared to 'time_limit'. Once some permutation is found
    that is equal or less than 'time_limit' the function returns the members
    of that permutation in a list and terminates. If no solution is found
    in the permutations of [bunnies], a new set is created from combinations
    of the set [bunnies] with length len(bunnies) - 1 and all permutations
    of all those combinations are considered. Again, if no solution is found
    combinations from the set [bunnies] of length len(bunnies) - 2.. and so
    forth, until a solution is found. If still no solution exists the function
    returns an empty list.

    Bellman-Ford solves the shortest paths for each vertex V at O(E*V); for
    the complete graph G, this is O(V**3). Solving the hamiltonian cycle
    in the metric closure is equivalent to the asymmetric traveling salesman
    problem, the brute force approach here for all combinations of bunnies
    is O(n!) for 'n' nodes.
    '''
    V_i = len(times)  # number of spaces in initial corridor
    bunnies = [i + 1 for i in range(V_i - 2)]
    for f in reversed(bunnies):
        for rescued in combinations(bunnies, f):
            rescued = list(rescued)
            corridor = [0]
            corridor.extend(rescued)
            corridor.append(V_i - 1)
            G = EdgeWeightedDigraph(V_i, times, corridor)
            spt = [object for _ in range(V_i)]
            G_mc = [[int() for _ in range(V_i)] for _ in range(V_i)]
            for i in corridor:
                spt[i] = BellmanFordSP(G, i)
                if spt[i].has_negative_cycle():
                    return [b - 1 for b in bunnies]
                
                for v in corridor:
                    if v != i:
                        G_mc[i][v] = path_weight(spt[i].path_to(v))

            # Brute force examination of paths in G_mc
            for p in permutations(rescued):
                p = list(p)
                p.append(V_i - 1)

                weight = 0
                v = 0
                for w in p:
                    weight += G_mc[v][w]
                    v = w
                if weight <= time_limit:
                    return [b - 1 for b in rescued]
    return []

def path_weight(path):
    weight = 0
    for e in path:
        weight += e.weight
    return weight

class EdgeWeightedDigraph(object):
    def __init__(self, V, lists=None, ifunc=None):
        self._V = V
        self._adj = [Counter() for _ in range(V)]

        if lists is not None:
            if ifunc is None:
                ifunc = range(self._V)
            for v in ifunc:
                for w in filter(lambda i: i != v, ifunc):
                    e = DirectedEdge(v, w, lists[v][w])
                    self.add_edge(e)

    @property
    def V(self):
        return self._V

    def adj(self, v):
        return self._adj[v].elements()

    def add_edge(self, e):
        v = e.from_v
        self._adj[v][e] += 1

class EdgeWeightedDirectedCycle(object):
    def __init__(self, G):
        self._marked = [bool(False) for _ in range(G.V)]
        self._edge_to = [None for _ in range(G.V)]
        self._cycle = None
        self._on_stack = [bool(False) for _ in range(G.V)]
        for v in range(G.V):
            if not self.marked[v]:
                self.dfs(G, v)

    @property
    def marked(self):
        return self._marked

    @property
    def edge_to(self):
        return self._edge_to

    @property
    def cycle(self):
        return self._cycle

    @property
    def on_stack(self):
        return self._on_stack

    def dfs(self, G, v):
        self.on_stack[v] = True
        self.marked[v] = True
        for e in G.adj(v):
            if self.has_cycle():
                return None
            w = e.to_w
            if not self.marked[w]:
                self.edge_to[w] = e
                self.dfs(G, w)
                if self.on_stack[w]:
                    self.cycle.appendleft(e)
                    return None
            elif self.on_stack[w]:
                self._cycle = deque()
                x = self.edge_to[w]
                while x is not None and x.from_w != w:
                    self.cycle.appendleft(x)
                    x = self.edge_to[x.from_w]
                self.cycle.appendleft(e)
                return None
        self.on_stack[v] = False

    def has_cycle(self):
        return self.cycle is not None

class BellmanFordSP(object):
    def __init__(self, G, s):
        self._edge_to = [None for _ in range(G.V)]
        self._dist_to = [float('inf') for _ in range(G.V)]
        self._on_queue = [bool(False) for _ in range(G.V)]
        self._queue = deque()
        self._cost = 0
        self._cycle = None

        self.dist_to[s] = 0.0
        self.queue.append(s)
        self.on_queue[s] = True

        while len(self.queue) != 0 and not self.has_negative_cycle():
            v = self.queue.popleft()
            self.on_queue[v] = False
            self.relax(G, v)

    @property
    def edge_to(self):
        return self._edge_to

    @property
    def dist_to(self):
        return self._dist_to

    @property
    def on_queue(self):
        return self._on_queue

    @property
    def queue(self):
        return self._queue

    @property
    def cost(self):
        return self._cost

    def relax(self, G, v):
        for e in G.adj(v):
            w = e.to_w
            if self.dist_to[w] > self.dist_to[v] + e.weight:
                self.dist_to[w] = self.dist_to[v] + e.weight
                self.edge_to[w] = e
                if not self.on_queue[w]:
                    self.queue.append(w)
                    self.on_queue[w] = True
            if self.cost % G.V == 0:
                self.find_negative_cycle()
            self._cost += 1

    def has_path_to(self, v):
        return self.dist_to[v] < float('inf')

    def path_to(self, v):
        if not self.has_path_to(v):
            return None
        path = deque()
        e = self.edge_to[v]
        while True:
            if e is None:
                break
            path.appendleft(e)
            e = self.edge_to[e.from_v]
        return list(path)

    def find_negative_cycle(self):
        V = len(self.edge_to)
        spt = EdgeWeightedDigraph(V)
        for v in range(V):
            if self.edge_to[v] is not None:
                spt.add_edge(self.edge_to[v])

        cf = EdgeWeightedDirectedCycle(spt)

        self._cycle = cf.cycle

    def has_negative_cycle(self):
        return self._cycle is not None

    def negative_cycle(self):
        return list(self._cycle)

if __name__  == '__main__':
    times = [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], \
        [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]]
    rescued = solution(times, 1)
    print(rescued)