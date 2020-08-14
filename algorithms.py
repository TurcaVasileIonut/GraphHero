import networkx as nx
from queue import PriorityQueue


# this check if the graph is eulerian
def is_eulerian(g):
    if g.is_directed():
        return (all(g.in_degree(n) == g.out_degree(n) for n in g) and
                nx.is_strongly_connected(g))
    return all(d % 2 == 0 for v, d in g.degree()) and nx.is_connected(g)


# this is a DFS that mark all the nodes in the current component
def connected_components(g, node, seen):
    # access all of the neighbors of the node
    for to in g[node]:
        # check if current neighbor is visited
        if to not in seen:
            # if is not visited, mark it and check his neighbors
            seen.add(to)
            connected_components(g, to, seen)


# this count the number of connected components
def number_connected_components(g):
    seen = set()
    cnt = int(0)

    # check liniar if a node is not in a component
    for node in g:
        if node not in seen:
            # if this is not in a previously visited component means that I discovered a new component
            cnt = cnt + 1  # count the number of components
            connected_components(g, node, seen)  # mark all the nodes in this component
    return cnt


# this is a DFS that sort topological the nodes
def dfs(g, node, seen, discovered):
    seen.add(node)
    for to in g[node]:
        if to not in seen:
            dfs(g, to, seen, discovered)
    discovered.append(node)


# this is a DFS that check what nodes (are before in the discovered list) are reachable from current node
def dfs2(g, node, seen2):
    seen2.add(node)
    for to in g[node]:
        if to not in seen2:
            dfs2(g, to, seen2)


# count the number of strong connected components
def number_strong_connected_components(g):
    cnt = 0

    seen = set()
    discovered = list()
    g2 = nx.DiGraph()
    for node in g:
        for to in g[node]:
            g2.add_edge(to, node)
    # sort topological the nodes
    for node in g:
        if node not in seen:
            dfs(g, node, seen, discovered)

    # check what nodes (are before in the discovered list) are reachable from current node
    seen2 = set()
    while len(discovered) > 0:
        if discovered[len(discovered) - 1] not in seen2:
            cnt = cnt + 1
            dfs2(g2, discovered[len(discovered) - 1], seen2)
        discovered.pop()

    return cnt


# calculates the distances and the optimal meeting point between two nodes
def dijkstra(g, node1, node2, is_weighted):
    # in dist1 are distances from first node to all the others
    dist1 = {}
    # in dist2 are distances from second node to all the others
    dist2 = {}
    inf = 999999999999999999999999999999

    # initial set all the values to inf
    for node in g:
        dist1[node] = inf
        dist2[node] = inf

    # put first node in the priority queue
    q = PriorityQueue()
    q.put([0, node1])
    # distance from first node to himself is always 0
    dist1[node1] = 0
    # in seen1 is memorized if a node was visited
    seen1 = set()

    if not is_weighted:
        # if the graph is not weighted, distance between the nodes of an edge is 1
        while not q.empty():
            node = q.get()

            if node[1] in seen1:
                # if I was before in this node, means that there is no reason of processing it again
                continue

            # mark that I was in this node
            seen1.add(node[1])

            for to in g.neighbors(node[1]):
                # check if a neighbour of current node is at a smaller distance than it was before
                if dist1[to] > dist1[node[1]] + 1:
                    dist1[to] = dist1[node[1]] + 1
                    q.put([dist1[to], to])

    else:
        # if the graph is weighted, distance between the nodes of an edge is the weight of the edge
        while not q.empty():
            node = q.get()

            if node[1] in seen1:
                # if I was before in this node, means that there is no reason of processing it again
                continue

            # mark that I was in this node
            seen1.add(node[1])

            for to in g.neighbors(node[1]):
                # check if a neighbour of current node is at a smaller distance than it was before
                cost = int(g[node[1]][to]['weight'])
                if dist1[to] > dist1[node[1]] + cost:
                    dist1[to] = dist1[node[1]] + cost
                    q.put([dist1[to], to])

    # repeat the above algorithm for second node
    q.put([0, node2])
    dist2[node2] = 0
    seen2 = set()
    if not is_weighted:
        while not q.empty():
            node = q.get()

            if node[1] in seen2:
                continue
            seen2.add(node[1])

            for to in g.neighbors(node[1]):
                if dist2[to] > dist2[node[1]] + 1:
                    dist2[to] = dist2[node[1]] + 1
                    q.put([dist2[to], to])
    else:
        while not q.empty():
            node = q.get()

            if node[1] in seen2:
                continue
            seen2.add(node[1])

            for to in g.neighbors(node[1]):
                cost = int(g[node[1]][to]['weight'])
                if dist2[to] > dist2[node[1]] + cost:
                    dist2[to] = dist2[node[1]] + cost
                    q.put([dist2[to], to])

    # initially, it is expected that is not a meeting point
    meeting_node = '-1'
    meeting_dist = inf
    meeting_dif = inf

    for node in g:
        # check all the nodes before
        if dist1[node] + dist2[node] < meeting_dist:
            # if total distance traveled is less than from actual meeting node, this becomes the optimal meeting node
            meeting_dist = dist1[node] + dist2[node]
            meeting_node = node
            meeting_dif = abs((dist1[node] - dist2[node]))
        else:
            # if the distance is equal, but it is closer to middle, this becomes the optimal meeting point
            if dist1[node] + dist2[node] == meeting_dist and abs((dist1[node] - dist2[node])) < meeting_dif:
                meeting_dist = dist1[node] + dist2[node]
                meeting_node = node
                meeting_dif = abs((dist1[node] - dist2[node]))

    # return the calculated meeting point and the distances from first to second and from second to first
    return [meeting_node, dist1[node2], dist2[node1]]


# this calculate the minimum partial tree
def partial_tree(g, is_weighted):
    dist = {}
    inf = 9999999999999999999999999999
    for node in g:
        dist[node] = inf

    # in seen is memorized if a node is added in the tree
    seen = set()
    q = PriorityQueue()
    from_edge = {}

    # there can be more than one component
    # a node from every component will be in comp
    comp = list()

    # start the searching from the first node in the graph
    while True:
        # if an unvisited node was visited, unvisited take the value of the node
        unvisited = -1
        for node in g:
            if node not in seen:
                dist[node] = 0
                q.put([0, node])
                unvisited = node
                break

        if unvisited == -1:
            break

        comp.append(unvisited)

        # at every step, the nearest node from the first is processed
        if not is_weighted:
            # if the graph is not weighted, the cost of edges is 1
            while not q.empty():
                node = q.get()

                if node[1] in seen:
                    # there is no reason for processing a node twice or more
                    continue

                # this node is processed now
                seen.add(node[1])

                # check if the total cost is less if one or more of the neighbors are connected at
                # tree with a edge from current node
                for to in g.neighbors(node[1]):
                    if dist[to] > dist[node[1]] + 1:
                        dist[to] = dist[node[1]] + 1
                        q.put([dist[to], to])
                        from_edge[to] = node[1]
        else:
            # if the graph is weighted, the cost of an edge is the weight of the edge
            while not q.empty():
                node = q.get()

                if node[1] in seen:
                    # there is no reason for processing a node twice or more
                    continue

                # this node is processed now
                seen.add(node[1])

                # check if the total cost is less if one or more of the neighbors are connected at
                # tree with a edge from current node
                for to in g.neighbors(node[1]):
                    cost = int(g[node[1]][to]['weight'])
                    if dist[to] > dist[node[1]] + cost:
                        dist[to] = dist[node[1]] + cost
                        q.put([dist[to], to])
                        from_edge[to] = (node[1], cost)

    # create the list of edges
    edges = []
    if is_weighted:
        # if the graph is weighted, the list will contain the weights of edges
        for node1 in from_edge:
            edges.append((node1, from_edge[node1][0], from_edge[node1][1]))
        for i in range(1, len(comp)):
            edges.append((comp[i], comp[i - 1], 1))
    else:
        for node1 in from_edge:
            edges.append((node1, from_edge[node1]))
        for i in range(1, len(comp)):
            edges.append((comp[i], comp[i - 1]))

    return edges
