import networkx as nx
import community
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

def preprocess_VIG(formula, VIG):
    """
    Builds VIG.
    """
    import itertools
    for cn in range(len(formula)):
        if len(formula[cn]) != 1:
            weight_vig = 2.0 / (len(formula[cn]) * (len(formula[cn])-1) )
            for comb in itertools.combinations(formula[cn], 2):
                i, j = comb
                if VIG.has_edge(abs(i), abs(j)):
                    weight_edge = VIG.get_edge_data(abs(i), abs(j))['weight']
                    w = weight_edge + weight_vig
                    VIG.add_edge(abs(i), abs(j), weight=w)
                else:
                    VIG.add_edge(abs(i), abs(j), weight=weight_vig)

def get_modularity(VIG):
    part_VIG = community.best_partition(VIG, weight="weight")
    mod_VIG = community.modularity(part_VIG, VIG, weight="weight") # Modularity of VIG
    num_parts = len(np.unique(np.array(list(part_VIG.values()))))

    groups, group_sizes = np.unique(np.array(list(part_VIG.values())), return_counts=True)

    fig, ax = plt.subplots()

    ax.hist(group_sizes, bins=10)
    ax.set_xlabel("Tamaño de la comunidad")
    ax.set_ylabel("# Comunidades")

    return mod_VIG, num_parts, group_sizes, (fig, ax)

def get_clustering(VIG):
    clust_nodes = nx.clustering(VIG, weight=None)

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

def sat_to_VIG(source):
    print(f"Reading {source}")
    cnf = open(source)
    content = cnf.readlines()
    while content[0].split()[0] == 'c':
        content = content[1:]
    while len(content[-1].split()) <= 1:
        content = content[:-1]

    # Paramters
    parameters = content[0].split()
    formula = content[1:]
    formula = to_int_matrix(formula)
    num_vars = int(parameters[2])
    num_clause = int(parameters[3])
    #print (num_vars)

    VIG = nx.Graph()
    VIG.add_nodes_from(range(num_vars + 1)[1:])
    preprocess_VIG(formula, VIG) # Build a LIG
    return VIG

def create_VIG(path):
    print(f"Reading {path}")
    cnf = open(path)
    content = cnf.readlines()
    cnf.close()

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

    return VIG