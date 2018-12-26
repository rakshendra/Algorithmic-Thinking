"""
Project-2
 - BFS
 - Connected Components
 - Reselience Calculation
"""
from collections import deque

def bfs_visited(ugraph, start_node):
    """
    Visit neigboring nodes from start_node and return set of visited nodes
    """
    queue = deque()
    visited = set([start_node])
    queue.append(start_node)
    
    while queue:
        node = queue.popleft()
        for neighbor in ugraph[node]:
            if not visited.__contains__(neighbor):
                visited.add(neighbor)
                queue.append(neighbor)
    return visited

def cc_visited(ugraph):
    """
    return a list of connected components in ugraph, where each compnent 
    is a set of nodes
    """
    remaining_nodes = set(ugraph.keys())
    connected_comps = []
    while remaining_nodes:
        node = next(iter(remaining_nodes));
        visited = bfs_visited(ugraph, node)
        connected_comps.append(set(visited))
        for v_node in visited:
            remaining_nodes.remove(v_node)
    return connected_comps;
    
def largest_cc_size(ugraph):
    """
    Return size of the largest connected component for given graph
    """
    comps = cc_visited(ugraph)
    max_size = 0;
    for comp in comps:
        if len(comp) > max_size:
            max_size = len(comp)
    return max_size

def remove_node(ugraph, to_be_removed):
    """
    removes a node from the graph completely
    """
    del ugraph[to_be_removed]
    for node in ugraph:
        neighbors = ugraph[node]
        neighbors.discard(to_be_removed)
    return ugraph

def compute_resilience(ugraph, attack_order):
    """
    Compute reselience which is the size of largest cc in graph, after 
    removal of nodes from the graph
    """
    
    resilience = [largest_cc_size(ugraph)]
    for node in attack_order:
        ugraph = remove_node(ugraph, node)
        resilience.append(largest_cc_size(ugraph))
    return resilience