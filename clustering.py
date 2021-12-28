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