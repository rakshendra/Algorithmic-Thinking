import random as rand
import alg_upa_trial as alg_upa
import alg_application2_provided as loader
import project_2 as helper
import matplotlib.pyplot as plotter
import timeit

#Application2.py
def make_complete_graph(num_nodes):
    """
    Construct and return an undirected graph where all the nodes are 
    interconnected
    """
    undirected_graph = {}
    if num_nodes > 0:
        for num1 in range(num_nodes):
            temp_set = set([])
            for num2 in range(num_nodes):
                if num2!= num1:
                    temp_set.add(num2)
            undirected_graph[num1] = temp_set
    return undirected_graph

def er_algo_graph(num_nodes, prob):
    graph = {key: set() for key in xrange(num_nodes)}
    for node1 in xrange(num_nodes):
        for node2 in xrange(num_nodes):
            if(node1 != node2):
                if rand.random() < prob:
                    graph[node1].add(node2)
                    graph[node2].add(node1)
    return graph

def upa_algo_graph(total_nodes, initial_nodes):
    if initial_nodes > total_nodes:
        print('Error: initial nodes cannot be more than total nodes')
        
    graph = make_complete_graph(initial_nodes)
    upa = alg_upa.UPATrial(initial_nodes)
    for node in xrange(initial_nodes, total_nodes):
        neighbors = upa.run_trial(initial_nodes)
        graph[node] = neighbors
        for neighbor in neighbors:
            graph[neighbor].add(node)
    return graph

def count_edges(graph):
    edges=0
    for node in graph:
        edges = edges+len(graph[node])
    return edges/2

def random_order(graph):
    nodes = graph.keys()
    rand.shuffle(nodes)
    return nodes

def question1(cn_graph, er_graph, upa_graph, func, file_name, order_label):
    cn_res = helper.compute_resilience(loader.copy_graph(cn_graph), func(cn_graph))
    er_res = helper.compute_resilience(loader.copy_graph(er_graph), func(er_graph))
    upa_res = helper.compute_resilience(loader.copy_graph(upa_graph), func(upa_graph))
    
    x_num = range(len(cn_graph)+1)
    plotter.plot(x_num, cn_res, '-b', label='CN Graph')
    plotter.plot(x_num, er_res, '-y', label='ER Graph(p = 0.002)')
    plotter.plot(x_num, upa_res, '-g', label='UPA Graph(m = 3)')
    plotter.title('Resilience of Graph (%s)' % order_label)
    plotter.xlabel('# of nodes removed')
    plotter.ylabel('Resilience(Size of largest component in graph)')
    plotter.legend(loc='upper right')
    plotter.savefig(file_name)

def fast_targeted_order(graph):
    ugraph = loader.copy_graph(graph)
    num_of_nodes = len(ugraph)
    degree_sets = [set([]) for _ in xrange(num_of_nodes)]
    for node in ugraph:
        degree = len(ugraph[node])
        degree_sets[degree].add(node)
    order = []
    for k in xrange(num_of_nodes-1, -1,-1):
        while len(degree_sets[k]) > 0:
            u = degree_sets[k].pop()
            for neighbor in ugraph[u]:
                d = len(ugraph[neighbor])
                degree_sets[d].remove(neighbor)
                degree_sets[d-1].add(neighbor)
            order.append(u)
            loader.delete_node(ugraph, u)
    return order    

def fast_targeted_order_(ugraph):
    new_graph = loader.copy_graph(ugraph)
    n = len(new_graph)
    degree_sets = [set([]) for _ in xrange(n)]
    for node in new_graph:
        d = len(new_graph[node])
        degree_sets[d].add(node)
    #print degree_sets
    attack_order = []
    for k in xrange(n - 1, -1, -1):
        #print degree_sets[k], degree_sets
        while len(degree_sets[k]) > 0:
            max_degree_node = degree_sets[k].pop()
            for node in new_graph[max_degree_node]:
                d = len(new_graph[node])
                degree_sets[d].remove(node)
                degree_sets[d-1].add(node)
            attack_order.append(max_degree_node)
            delete_node(new_graph, max_degree_node)
    return attack_order

def degrees_ugraph(ugraph):
    '''
    Take a ugraph
    return {node : degree}
    '''
    degrees = {}
    for node in ugraph:
        degrees[node] = len(ugraph[node])
    return degrees

def delete_node(ugraph, node):
    #delete a node from an undirected graph
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)

def measure_time(n, m, func):
    graph = upa_algo_graph(n,m)
    return timeit.timeit(lambda:func(graph), number=1)

def question3():
    x_range = range(10, 1000, 10)
    m=5
    y_targeted = [measure_time(n,m,loader.targeted_order) for n in x_range]
    y_fast_targeted = [measure_time(n,m,fast_targeted_order) for n in x_range]
    
    plotter.plot(x_range, y_targeted, '-b', label='Order: Targeted')
    plotter.plot(x_range, y_fast_targeted, '-g', label='Order: Fast Targeted')
    plotter.title('Targeted Order Performance(tested in Desktop Python)')
    plotter.xlabel('# of nodes in graph')
    plotter.ylabel('Time taken for execution(in Sec)')
    plotter.legend(loc='upper-right')
    plotter.savefig('q3-targeted-plot.png')

def main():
    cn_graph = loader.load_graph(loader.NETWORK_URL)
    edges = count_edges(cn_graph)
    num_of_nodes = len(cn_graph)
    
    print('Edges in CN graph %d' %edges)
    print('Nodes in CN graph %d' %num_of_nodes)
    
    prob=0.002 
    er_graph = er_algo_graph(num_of_nodes, prob)
    print('Edges in ER graph %d' % count_edges(er_graph))
    print('Nodes in ER graph %d' % len(er_graph))
    
    initial_nodes=3
    upa_graph = upa_algo_graph(num_of_nodes, initial_nodes)
    print('Edges in UPA graph %d' % count_edges(upa_graph))
    print('Nodes in UPA graph %d' % len(upa_graph))
    
    #question1(cn_graph, er_graph, upa_graph, random_order, 'q1-resilience-plot.png', 'using random_order')
    
    print()
    
    print("n2, n3")
    
    plotter.clf()
    question3()
    
    plotter.clf()
    #question1(cn_graph, er_graph, upa_graph, fast_targeted_order, 'q4-resilience-plot.png', 'using fast_targeted_order')

    
if __name__=="__main__":
    main()