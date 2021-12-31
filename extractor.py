import argparse

import vig_features
import degree_dist
import solvers
import clustering
import os
import numpy as np
import matplotlib.pyplot as plt
import shutil
import pandas as pd
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument("--all", help="Extract all features", action="store_true")
parser.add_argument("--mod", help="Modularity features", action="store_true")
parser.add_argument("--solvers", help="Solver features", action="store_true")
parser.add_argument("--clus", help="Clustering features", action="store_true")
parser.add_argument("--scale_free", help="Scale-Free features", action="store_true")
parser.add_argument("--path", help="Path to formula or family to be analyzed", type=str, required=("--compare" not in sys.argv))
parser.add_argument("--results", help="Path to save results", type=str, required=False, default="results")
parser.add_argument("--compare", help="Flag to compare two distributions", action="store_true")
parser.add_argument("--o", help="Path to original distribution", required=("--compare" in sys.argv))
parser.add_argument("--s", help="Path list to alternative distributions", required=("--compare" in sys.argv))

args = parser.parse_args()


# Check whether we are working over a family or a formula
if os.path.isdir(args.path):
    if os.listdir(args.path)[0][-4:] == ".cnf":
        family = True
        family_name = args.path.strip(os.path.sep).split(os.path.sep)[-1]

        try:
            df_extracted_values = pd.read_csv(os.path.join(args.results, f"results_{family_name}.csv"))
        except FileNotFoundError:
            df_extracted_values = pd.DataFrame([family_name], columns = ["Family name"])

        try:
            df_per_formula = pd.read_csv(os.path.join(args.results, "results_per_formula.csv"))
            list_formulas = set([path for path in os.listdir(args.path) if path[-4:] == ".cnf"])
            if list_formulas != set(list(df_per_formula.Formula)):
                raise ValueError("Las fórmulas no coinciden")
        except:
            df_per_formula = pd.DataFrame([path for path in os.listdir(args.path) if path[-4:] == ".cnf"], columns=["Formula"])
    else:
        raise TypeError("Source must be a CNF file or a directory containing CNF files")
else:
    if args.path[-4:] == ".cnf":
        family = False
        _, formula_name = os.path.split(args.path)
        try:
            df_extracted_values = pd.read_csv(os.path.join(args.results, f"results_{formula_name}.csv"))
        except FileNotFoundError:
            df_extracted_values = pd.DataFrame([formula_name], columns = ["Formula name"])
    else:
        raise TypeError("Source must be a CNF file or a directory containing CNF files")

from pathlib import Path
path_res = Path(args.results)
path_res.mkdir(parents=True, exist_ok=True)


# Load VIG graph, used for Modularity and Clustering Coefficient
if args.mod or args.clus or args.all:
    if not family:
        print(f"Working on formula \'{formula_name}\'")
        import time
        inicio = time.time()
        VIG = vig_features.sat_to_VIG_mod(args.path)
        fin = time.time()
        time_orig = fin-inicio

        print(f"Time loading formula: {time_orig}s")

        # inicio = time.time()
        # VIG_comb = modularity.sat_to_VIG(args.path)
        # fin = time.time()
        # time_mod = fin-inicio

        # print(f"Time loading formula: {time_orig}s and {time_mod}s")
        # # print(VIG[1000])
        # # print(VIG_comb[1000])
        # import networkx as nx
        # print(nx.algorithms.isomorphism.is_isomorphic(VIG, VIG_comb, edge_match=nx.algorithms.isomorphism.numerical_edge_match(attr="weight", default=1)))
        # exit()
    else:
        print(f"Working on family \'{family_name}\'")
        VIGs = {path: vig_features.sat_to_VIG(os.path.join(args.path, path)) for path in os.listdir(args.path) if path[-4:] == ".cnf"}


if args.mod or args.all:
    if family:
        mods = {}
        num_comm = {}
        for i, form in enumerate(VIGs.keys()):
            mod_VIG, num_parts, gs, fig = vig_features.get_modularity(VIGs[form])
            mods[form] = mod_VIG
            num_comm[form] = num_parts
            # fig[1].set_title(form)
            # fig[0].savefig(f"{form}.png")
            plt.close(fig[0])
            
            if i == 0:
                group_sizes = gs
            else:
                group_sizes = np.concatenate([group_sizes, gs], axis=0)


        mod_df = pd.DataFrame.from_dict(mods, orient="index", columns=["mod"])
        if "mod" in df_per_formula.columns:
            df_per_formula = df_per_formula.drop(columns=["mod"])
        df_per_formula = df_per_formula.set_index("Formula", drop=False).join(mod_df)
        del mod_df

        group_df = pd.DataFrame(np.array(group_sizes).reshape((-1,1)), columns=["group_sizes"])
        group_df.to_csv(os.path.join(args.results, "group_sizes_agg.csv"), index=False)

        mod_values = np.array(list(mods.values()))
        mean_mod = np.mean(mod_values)
        std_mod = np.std(mod_values)

        num_comm_values = np.array(list(num_comm.values()))
        mean_num_comm = np.mean(num_comm_values)
        std_num_comm = np.std(num_comm_values)

        df_extracted_values["mod_mean"] = [mean_mod]
        df_extracted_values["mod_std"] = [std_mod]
        df_extracted_values["#comm_mean"] = [mean_num_comm]
        df_extracted_values["#comm_std"] = [std_num_comm]

        plt.hist(group_sizes, bins=10, edgecolor="black")
        plt.xlabel("Tamaño de la comunidad")
        plt.ylabel("# Comunidades")
        hist_range = np.linspace(0,np.max(group_sizes),11, dtype="int")
        hist_labels = [f"[{hist_range[i]}-{hist_range[i+1]-1}]" for i in range(len(hist_range)-1)]
        plt.xticks((hist_range-(np.max(group_sizes)/(2*10)))[1:],
                    labels=hist_labels,rotation=45)
        plt.title(family_name.upper())
        plt.tight_layout()
        plt.savefig(os.path.join(args.results, f"{family_name}-comm.png"))
        plt.close() 
    else:
        mod_VIG, num_parts, gs, fig = vig_features.get_modularity(VIG)

        plt.close(fig[0])
        
        df_extracted_values["mod"] = [mod_VIG]
        df_extracted_values["#comm"] = [num_parts]

        plt.hist(gs, bins=np.arange(0, np.max(gs)+1, int(np.max(gs)/10)), edgecolor="black")
        plt.xlabel("Tamaño de la comunidad")
        plt.ylabel("# Comunidades")
        hist_range = np.arange(0, np.max(gs)+1, int(np.max(gs)/10))
        hist_labels = [f"[{hist_range[i]}-{hist_range[i+1]-1}]" for i in range(len(hist_range)-1)]
        plt.xticks((hist_range-(np.max(gs)/(2*10)))[1:],
                    labels=hist_labels, rotation=45)
        plt.title(formula_name)
        plt.tight_layout()
        plt.savefig(os.path.join(args.results, f"{formula_name}-comm.png"))
        plt.close()
        
    
if args.clus or args.all:
    if family:
        clusts = {}
        for i, form in enumerate(VIGs.keys()):
            clust, clust_v, fig = clustering.get_clustering(VIGs[form])
            clusts[form] = clust
            if i == 0:
                clust_values_all = clust_v
            else:
                clust_values_all = np.concatenate((clust_values_all, clust_v), axis=0)

            fig[1].set_title(form)
            plt.close(fig[0])

        clust_values = np.array(list(clusts.values()))
        mean_clust = np.mean(clust_values)
        std_clust = np.std(clust_values)

        clust_df = pd.DataFrame.from_dict(clusts, orient="index", columns=["clust"])
        if "clust" in df_per_formula.columns:
            df_per_formula = df_per_formula.drop(columns=["clust"])
        df_per_formula = df_per_formula.set_index("Formula", drop=False).join(clust_df)
        del clust_df

        clust_values_df = pd.DataFrame(clust_values_all.reshape((-1,1)), columns=["clust_values"])
        clust_values_df.to_csv(os.path.join(args.results, "clust_values_agg.csv"), index=False)

        df_extracted_values["clust_mean"] = [mean_clust]
        df_extracted_values["clust_std"] = [std_clust]

        plt.hist(clust_values_all, bins=20, range=[0,1], edgecolor="black")
        hist_range = np.linspace(0,1,21)
        hist_labels = [f"[{round(hist_range[i], 2)}-{round(hist_range[i+1], 2)})" for i in range(len(hist_range)-1)]
        plt.xticks((hist_range-(1/(2*20)))[1:], labels=hist_labels, rotation=75)
        plt.xlabel("Clustering Coefficient")
        plt.ylabel("# Nodos")
        plt.title(family_name.upper())
        plt.xlim([0,1])
        plt.tight_layout()
        plt.savefig(os.path.join(args.results, f"{family_name}-clustering.png"))
        plt.close()
    else:
        average_clust, _, fig = clustering.get_clustering(VIG)

        df_extracted_values["clust"] = [average_clust]

        fig[0].savefig(os.path.join(args.results, f"{formula_name}-clustering.png"))
        plt.close(fig[0])


if args.all or args.clus or args.mod:
    del VIGs


if args.scale_free or args.all:
    alpha, kmin, error, k_err = degree_dist.degree_dist(args.path, args.results)
    df_extracted_values["powerlaw-alpha"] = [alpha]
    df_extracted_values["powerlaw-k_min"] = [kmin]
    df_extracted_values["powerlaw-error"] = [error]
    df_extracted_values["powerlaw-k_err"] = [k_err]



if args.clus or args.mod or args.scale_free or args.all:
    if family:
        if args.clus or args.mod or args.scale_free or args.all:
            df_extracted_values.to_csv(os.path.join(args.results, f"results.csv"), index=False)
    else:
        df_extracted_values.to_csv(os.path.join(args.results, f"results_{formula_name}.csv"), index=False)


if args.solvers or args.all:
    solver_list = [solvers.Glucose(), solvers.MapleLCM(), solvers.MapleSAT(), solvers.Lingeling(), solvers.Cadical()]
    time_limit = 1000
    max_retries=3

    if family:
        dfs = {}
        for form in os.listdir(args.path):
            print(f"Solving {form}: ")
            results = []
            for i, solv in enumerate(solver_list):
                for rt in range(max_retries):
                    try:
                        result, cpu_time = solv.solve(os.path.join(args.path, form), time_limit=time_limit)
                    except:
                        e = sys.exc_info()[0]
                        if rt <= max_retries - 1:
                            time.sleep(0.5)
                            continue
                        else:
                            raise e
                    break
                # result, cpu_time = solv.solve(os.path.join(args.path, form), time_limit=time_limit)
                print(f"\t{solv.name} --> {result} in {cpu_time}s")
                if result != "INDET":
                    par2 = cpu_time
                else:
                    par2 = 2.0*time_limit

                results.append([form, solv.name, result, par2])

            df_results = pd.DataFrame(results, columns=["Formula", "Solver", "Result", "CPU_time"])
            dfs[form] = df_results
            
            print(df_results)
            print("\n")


        merged_df = pd.concat(dfs.values(), axis=0)
        merged_df.to_csv(os.path.join(args.results, f"solvers_per_formula.csv"), index=False)
        type_result = pd.CategoricalDtype(categories=["SAT", "UNSAT", "INDET"])
        merged_df.Result = merged_df.Result.astype(type_result)
        merged_df = pd.get_dummies(merged_df, columns=["Result"], prefix=["#"])

        solvers_per_form_df = merged_df.groupby(by="Formula").agg({"#_SAT":"sum", "#_UNSAT":"sum", "#_INDET":"sum"})
        if "#_SAT" in df_per_formula.columns:
            df_per_formula = df_per_formula.drop(columns=["#_SAT", "#_UNSAT", "#_INDET"])
        df_per_formula = df_per_formula.set_index("Formula", drop=False).join(solvers_per_form_df)
        del solvers_per_form_df

        merged_df = merged_df.groupby(by="Solver").agg({"CPU_time": 'sum', "#_SAT":"sum", "#_UNSAT":"sum", "#_INDET":"sum"}).sort_values(by="CPU_time")
        merged_df.to_csv(os.path.join(args.results, f"result_solvers.csv"))

    else:
        print(f"Solving {formula_name}: ")
        results = []
        for i, solv in enumerate(solver_list):
            result, cpu_time = solv.solve(args.path, time_limit=time_limit)
            print(f"\t{solv.name} --> {result} in {cpu_time}s")
            if result != "INDET":
                par2 = cpu_time
            else:
                par2 = 2.0*time_limit

            results.append([solv.name, result, par2])

        df_results = pd.DataFrame(results, columns=["Solver", "Result", "CPU_time"])
        df_results = df_results.sort_values(by="CPU_time").reset_index(drop=True)
        df_results.to_csv(os.path.join(args.results, f"{formula_name}-solvers.csv"), index=False)

if family:
    df_per_formula = df_per_formula.drop(columns=["Formula"])
    df_per_formula.to_csv(os.path.join(args.results, f"results_per_formula.csv"), index=True)