import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def to_int_matrix(formula):
    for i in range(len(formula)):
        formula[i] = list(map(int, formula[i].split()))[: -1]
    return formula

def remove_duplicate(formula):
    cs = []
    new_formula = []
    num_clause = 0
    for line in formula:
        c = get_cl_string(line)
        if c not in cs:
            num_clause += 1
            new_formula.append(line)
            cs.append(c)
    return (new_formula, num_clause)

def get_cl_string(clause):
    s = ""
    clause.sort()
    for ele in clause:
        s += str(ele) + ","
    return s[:-1]

def get_vacuous(formula):
    vac = 0
    for line in formula:
        vac_loc = 0
        for ele in line:
            if -ele in line:
                vac_loc = 1
        if vac_loc == 1:
            vac += 1
    return vac

def preprocess_CVIG(formula, CVIG, num_vars):
    """
    Builds CVIG
    """
    for cn in range(len(formula)):
        w = 1/len(formula[cn])
        for var in formula[cn]:
            CVIG.add_edge(abs(var), cn + num_vars + 1, weight=w)

def preprocess_VIG(formula, VIG):
    """
    Builds VIG.
    """
    for cn in range(len(formula)):
        if len(formula[cn]) != 1:
            weight_vig = 2.0 / (len(formula[cn]) * (len(formula[cn])-1) )
            for i in range(len(formula[cn])-1):
                for j in range(len(formula[cn]))[i+1:]:
                    if VIG.has_edge(abs(formula[cn][i]), abs(formula[cn][j])):
                        weight_edge = VIG.get_edge_data(abs(formula[cn][i]), abs(formula[cn][j]))['weight']
                        w = weight_edge + weight_vig
                        VIG.add_edge(abs(formula[cn][i]), abs(formula[cn][j]), weight=w)
                    else:
                        VIG.add_edge(abs(formula[cn][i]), abs(formula[cn][j]), weight=weight_vig)

def get_clustering(VIG):
    clust_nodes = nx.clustering(VIG, weight="weight")

    clust_values = np.array(list(clust_nodes.values()))
    clust_mean = np.mean(clust_values)

    fig, ax = plt.subplots()
    ax.hist(clust_values, bins=20, range=[0,1], edgecolor="black")
    hist_range = np.linspace(0,1,21)
    hist_labels = [f"[{round(hist_range[i], 2)} - {round(hist_range[i+1], 2)})" for i in range(len(hist_range)-1)]
    ax.set_xticks((hist_range-(1/(2*20)))[1:])
    ax.set_xticklabels(hist_labels, rotation=75)
    ax.set_xlabel("Clustering Coefficient")
    ax.set_ylabel("# Nodos")
    ax.set_xlim([0.0,1.0])
    plt.tight_layout()
    
    return clust_mean, clust_values, (fig,ax)



if __name__=="__main__":
    # source = "data/cmu-bmc-longmult15.processed.cnf"
    source = "data/prueba/countbitsarray02_32.cnf"

    cnf = open(source)
    content = cnf.readlines()
    cnf.close()

    print ("Successfully read generated file {}".format(source))

    while content[0].split()[0] == 'c':
        content = content[1:]
    while len(content[-1].split()) <= 1:
        content = content[:-1]


    parameters = content[0].split()
    formula = content[1:]
    formula = to_int_matrix(formula)
    (formula, num_clauses) = remove_duplicate(formula)

    num_vars = int(parameters[2])

    assert (get_vacuous(formula) == 0)
    assert(num_vars != 0)
    assert(num_clauses == len(formula))

    VIG = nx.Graph()
    VIG.add_nodes_from(range(num_vars+1)[1:])

    preprocess_VIG(formula, VIG) # Build a VIG

    clust_VIG = nx.clustering(VIG, weight="weight")
    # for key,value in clust_VIG.items():
    #     print(key, value)

    print(clust_VIG)

    clust_values = clust_VIG.values()

    plt.hist(clust_values, bins=10)
    plt.show()




    # CVIG = nx.Graph()
    # CVIG.add_nodes_from(range(num_vars + num_clauses + 1)[1:])

    # preprocess_CVIG(formula, CVIG, num_vars) # Build a CVIG

    # from networkx.algorithms import bipartite

    # print(bipartite.average_clustering(CVIG))

    # print(bipartite.is_bipartite(CVIG))

    # import igraph

    # g = igraph.Graph.from_networkx(CVIG)

    # print(igraph.transitivity_local_undirected())