import alg_load_graph as loader
import project_1 as helper
import matplotlib.pyplot as plotter
import random as rand
import alg_dpa

    
def question1():
    graph = loader.load_graph(loader.CITATION_URL)
    normalized = normalize(helper.in_degree_distribution(graph))
    plot_graph(normalized, 'Citation', 'question1_graph.png', 'ro')

def question2():
    er_graph = er_algo_graph(1000, 0.1)
    normalized = normalize(helper.in_degree_distribution(er_graph))
    plot_graph(normalized, 'ER Graph', 'question2_graph.png', 'bo')
    
def question3():
    citation_graph = loader.load_graph(loader.CITATION_URL)
    total_nodes = len(citation_graph)
    initial_nodes = helper.compute_avg_out_degrees(citation_graph)
    print("Calculated values of n: {} m: {}".format(total_nodes, initial_nodes))

def question4():
    citation_graph = loader.load_graph(loader.CITATION_URL)
    total_nodes = len(citation_graph)
    initial_nodes = helper.compute_avg_out_degrees(citation_graph)
    dpa_graph = dpa_algo_graph(total_nodes, int(initial_nodes))
    normalized = normalize(helper.in_degree_distribution(dpa_graph))
    plot_graph(normalized, 'DPA', 'question3_graph.png', 'ro')
    
    
def normalize(distribution):
    total = float(sum(distribution.itervalues()))
    return {degree: count/total for degree, count in distribution.iteritems()}

def plot_graph(distribution, graph_name, file_name, color_shape):
    plotter.loglog()
    plotter.plot(distribution.keys(), distribution.values(),color_shape, ms=1.0)
    plotter.title('Normalized in-degree distribution of %s graph' %graph_name)
    plotter.xlabel('log In-degree')
    plotter.ylabel('log Normalized count')
    plotter.xlim(0,1000)
    plotter.grid()
    if file_name:
        plotter.savefig(file_name)
   
def er_algo_graph(num_nodes, prob):
    graph = {}
    for node1 in xrange(num_nodes):
        temp_set = set([])
        for node2 in xrange(num_nodes):
            if(node1 != node2):
                if rand.random() < prob:
                    temp_set.add(node2)
        graph[node1] = temp_set
    return graph

def dpa_algo_graph(total_nodes, initial_nodes):
    if initial_nodes > total_nodes:
        print('Error: initial nodes cannot be more than total nodes')
        
    synthetic_dag = helper.make_complete_graph(initial_nodes)
    dpa_alg = alg_dpa.DPATrial(initial_nodes)
    for node in xrange(initial_nodes, total_nodes):
        synthetic_dag[node] = dpa_alg.run_trial(initial_nodes)
    return synthetic_dag

            
question1()

plotter.clf()
question2()
plotter.clf()
question3()
question4()

