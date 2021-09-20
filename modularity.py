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
            # exit()
            # for i in range(len(formula[cn])-1):
            #     for j in range(len(formula[cn]))[i+1:]:
            #         if VIG.has_edge(abs(formula[cn][i]), abs(formula[cn][j])):
            #             weight_edge = VIG.get_edge_data(abs(formula[cn][i]), abs(formula[cn][j]))['weight']
            #             w = weight_edge + weight_vig
            #             VIG.add_edge(abs(formula[cn][i]), abs(formula[cn][j]), weight=w)
            #         else:
            #             VIG.add_edge(abs(formula[cn][i]), abs(formula[cn][j]), weight=weight_vig)

# vig = sat_to_VIG("data/aes_32_3_keyfind_2.processed.cnf")
# partition = community.best_partition(vig)
# # print(community.modularity(partition, vig))
# # print(partition)

# print(vig[1])


# # pos = nx.spring_layout(vig)
# # cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
# # nx.draw_networkx_nodes(vig, pos, partition.keys(), node_size=40, 
# #                         cmap=cmap, node_color=list(partition.values()))
# # nx.draw_networkx_edges(vig, pos, alpha=0.5)
# # plt.show()

# import numpy as np
# num_communities = len(np.unique(np.array(list(partition.values()))))
# print(num_communities)

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

def create_VIG_modified(path):
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



if __name__=="__main__":

    source = "data/bitverif/countbitsarray02_32.cnf"
    VIG = create_VIG(source)

    a, b, c, d = get_modularity(VIG)

    print(a)
    print(b)
    print(c)

    plt.show()