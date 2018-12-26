"""
Compute indegree of a graph and in-degree distribution
"""

EX_GRAPH0={0:set([1,2]),1:set([]), 2:set([])}
EX_GRAPH1={0:set([1,4,5]), 1:set([2,6]),2:set([3]),
           3:set([0]),4:set([1]),5:set([2]),6:set([])}
EX_GRAPH2={0:set([1,4,5]), 1:set([2,6]),2:set([3,7]),
           3:set([7]),4:set([1]),5:set([2]),6:set([]),
           7:set([3]),8:set([1,2]),9:set([0,4,5,6,7,3])}

def make_complete_graph(num_nodes):
    """
    Construct and return a complete directed graph where all the nodes are 
    interconnected
    """
    directed_graph = {}
    if num_nodes > 0:
        for num1 in range(num_nodes):
            temp_set = set([])
            for num2 in range(num_nodes):
                if num2!= num1:
                    temp_set.add(num2)
            directed_graph[num1] = temp_set
    return directed_graph
        
def compute_in_degrees(digraph):
    """
    return a dictionary containing degree of each node present in input digraph
    """
    in_degrees = {}
    for node in digraph:
        in_degrees[node]=0
    for node in digraph:
        for edge in digraph[node]:
            in_degrees[edge]+=1
    return in_degrees
    
def in_degree_distribution(digraph):
    """
    return a dictionary containing the distribution of in-degree of nodes 
    present in input digraph
    """
    in_degrees = compute_in_degrees(digraph)
    degree_distribution = {}
    for node in in_degrees:
        if degree_distribution.has_key(in_degrees[node]):
            degree_distribution[in_degrees[node]]+=1
        else:
            degree_distribution[in_degrees[node]]=1
    return degree_distribution

def compute_out_degrees(digraph):
    """
    return a dictionary containing degree of each node present in input digraph
    """
    out_degrees = {}
    for node in digraph:
        out_degrees[node]=0
    for node in digraph:
        out_degrees[node]= len(digraph[node])
        
    return out_degrees

def compute_avg_out_degrees(digraph):
    out_degrees = compute_out_degrees(digraph)
    total_out_deg = 0
    total_nodes = 0
    for node in out_degrees:
        total_nodes+=1;
        total_out_deg+=out_degrees[node]
    ans = float(total_out_deg)/total_nodes
    return round(ans)