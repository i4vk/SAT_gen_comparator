import argparse

from scipy.stats.stats import kendalltau
import modularity
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
import latex_table

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--results", help="Path to save results", type=str, required=False, default="results")
parser.add_argument("-o", "--orig", help="Path to original distribution", required=True)
parser.add_argument("-s", "--generator_list", help="Path list to generator distributions", required=True, nargs="+")
parser.add_argument("-l", "--light", help="Light execution (if you have low memory issues)", action="store_true", required=False)
parser.add_argument("--ignore_solvers", help="Exclude solvers from execution", action="store_true", required=False)

args = parser.parse_args()

def check_valid(path):
    valid = False
    if os.path.isdir(path):
        if os.listdir(args.orig)[0][-4:] == ".cnf":
            return True

    return valid


if not check_valid(args.orig):
    raise ValueError(f"{args.orig} is not a valid directory")

for dir in args.generator_list:
    if not check_valid(dir):
        raise ValueError(f"{dir} is not a valid directory")


from pathlib import Path
path_res = Path(args.results)
path_res.mkdir(parents=True, exist_ok=True)


def extract_mod(VIGs, family_name, df_result, df_per_formula):
    mods = {}
    num_comm = {}
    if type(VIGs) == dict:
        for i, form in enumerate(VIGs.keys()):
            mod_VIG, num_parts, gs, fig = modularity.get_modularity(VIGs[form])
            mods[form] = mod_VIG
            num_comm[form] = num_parts
            plt.close(fig[0])
            
            if i == 0:
                group_sizes = gs
            else:
                group_sizes = np.concatenate([group_sizes, gs], axis=0)
    elif type(VIGs) == list:
        for i, path in enumerate(VIGs):
            VIG_i = modularity.sat_to_VIG(path)
            _, form = os.path.split(path)
            mod_VIG, num_parts, gs, fig = modularity.get_modularity(VIG_i)
            mods[form] = mod_VIG
            num_comm[form] = num_parts
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

    group_sizes_df = pd.DataFrame(np.array(group_sizes).reshape((-1,1)), columns=["group_sizes"])

    mod_values = np.array(list(mods.values()))
    mean_mod = np.mean(mod_values)
    std_mod = np.std(mod_values)

    num_comm_values = np.array(list(num_comm.values()))
    mean_num_comm = np.mean(num_comm_values)
    std_num_comm = np.std(num_comm_values)

    df_result["mod_mean"] = [mean_mod]
    df_result["mod_std"] = [std_mod]
    df_result["#comm_mean"] = [mean_num_comm]
    df_result["#comm_std"] = [std_num_comm]

    plt.hist(group_sizes, bins=10, edgecolor="black")
    plt.xlabel("Tamaño de la comunidad", fontsize=16)
    plt.ylabel("# Comunidades", fontsize=16)
    hist_range = np.linspace(0,np.max(group_sizes),11, dtype="int")
    hist_labels = [f"[{hist_range[i]}-{hist_range[i+1]-1}]" for i in range(len(hist_range)-1)]
    plt.xticks((hist_range-(np.max(group_sizes)/(2*10)))[1:],
                labels=hist_labels,rotation=45)
    plt.title(family_name.upper())
    plt.tight_layout()
    plt.savefig(os.path.join(args.results, f"{family_name}-comm.png"))
    plt.close()

    return df_result, df_per_formula, group_sizes_df

def extract_clust(VIGs, family_name, df_result, df_per_formula):
    clusts = {}
    if type(VIGs) == dict:
        for i, form in enumerate(VIGs.keys()):
            clust, clust_v, fig = clustering.get_clustering(VIGs[form])
            clusts[form] = clust
            if i == 0:
                clust_values_all = clust_v
            else:
                clust_values_all = np.concatenate((clust_values_all, clust_v), axis=0)

            fig[1].set_title(form)
            plt.close(fig[0])
    elif type(VIGs) == list:
        for i, path in enumerate(VIGs):
            VIG_i = modularity.sat_to_VIG(path)
            clust, clust_v, fig = clustering.get_clustering(VIG_i)
            _, form = os.path.split(path)
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

    df_result["clust_mean"] = [mean_clust]
    df_result["clust_std"] = [std_clust]

    plt.hist(clust_values_all, bins=20, range=[0,1], edgecolor="black")
    hist_range = np.linspace(0,1,21)
    hist_labels = [f"[{round(hist_range[i], 2)}-{round(hist_range[i+1], 2)})" for i in range(len(hist_range)-1)]
    plt.xticks((hist_range-(1/(2*20)))[1:], labels=hist_labels, rotation=75)
    plt.xlabel("Clustering Coefficient", fontsize=16)
    plt.ylabel("# Nodos", fontsize=16)
    plt.title(family_name.upper())
    plt.xlim([0,1])
    plt.tight_layout()
    plt.savefig(os.path.join(args.results, f"{family_name}-clustering.png"))
    plt.close()

    return df_result, df_per_formula, clust_values_df

def extract_scale_free(path, df_result):
    alpha, kmin, error, k_err = degree_dist.degree_dist(path, args.results)
    df_result["powerlaw-alpha"] = [alpha]
    df_result["powerlaw-k_min"] = [kmin]
    df_result["powerlaw-error"] = [error]
    df_result["powerlaw-k_err"] = [k_err]

    return df_result

def extract_solvers(path, df_per_formula):
    if not os.path.isfile(os.path.join(args.results, f"solvers_per_formula_{path.strip(os.path.sep).split(os.path.sep)[-1]}.csv")):
        solver_list = [solvers.Glucose(), solvers.MapleLCM(), solvers.MapleSAT(), solvers.Lingeling(), solvers.Cadical()]
        time_limit = 1500
        max_retries=3
        
        dfs = {}
        count = 0
        for form in os.listdir(path):
            print(f"Solving {form}: ")
            results = []
            for i, solv in enumerate(solver_list):
                for rt in range(max_retries):
                    try:
                        result, cpu_time = solv.solve(os.path.join(path, form), time_limit=time_limit)
                    except:
                        e = sys.exc_info()[0]
                        if rt <= max_retries - 1:
                            time.sleep(0.5)
                            continue
                        else:
                            raise e
                    break
                
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
            count += 1


        merged_df = pd.concat(dfs.values(), axis=0)
        print(merged_df)
        merged_df.to_csv(os.path.join(args.results, f"solvers_per_formula_{path.strip(os.path.sep).split(os.path.sep)[-1]}.csv"), index=False)
    else:
        merged_df = pd.read_csv(os.path.join(args.results, f"solvers_per_formula_{path.strip(os.path.sep).split(os.path.sep)[-1]}.csv"))
    print(merged_df.dtypes)
    result_sat_unsat = merged_df["Result"]
    type_result = pd.CategoricalDtype(categories=["SAT", "UNSAT", "INDET"])
    merged_df.Result = merged_df.Result.astype(type_result)
    merged_df = pd.get_dummies(merged_df, columns=["Result"], prefix=["#"])

    solvers_per_form_df = merged_df.groupby(by="Formula").agg({"#_SAT":"sum", "#_UNSAT":"sum", "#_INDET":"sum"})
    if "#_SAT" in df_per_formula.columns:
        df_per_formula = df_per_formula.drop(columns=["#_SAT", "#_UNSAT", "#_INDET"])
    df_per_formula = df_per_formula.set_index("Formula", drop=False).join(solvers_per_form_df)
    del solvers_per_form_df

    def sat_unsat(row):
        if row["#_SAT"] > 0:
            return "SAT"
        elif row["#_UNSAT"] > 0:
            return "UNSAT"
        else:
            return "INDET"

    def search_sat_unsat(row, df_per_formula):
        type_form = df_per_formula.query("Formula == @row.Formula")["Type_formula"].values[0]
        return type_form


    df_per_formula["Type_formula"] = df_per_formula.apply(sat_unsat, axis=1)
    merged_df["Type_formula"] = merged_df.apply(search_sat_unsat, args=(df_per_formula,), axis=1)
    merged_df_type = merged_df.groupby(by=["Solver", "Type_formula"]).agg({"CPU_time": 'sum', "#_SAT":"sum", "#_UNSAT":"sum", "#_INDET":"sum"}).sort_values(by="CPU_time")

    merged_df = merged_df.groupby(by="Solver").agg({"CPU_time": 'sum', "#_SAT":"sum", "#_UNSAT":"sum", "#_INDET":"sum"}).sort_values(by="CPU_time")

    sat_times = merged_df_type.query("Type_formula == 'SAT'")
    unsat_times = merged_df_type.query("Type_formula == 'UNSAT'")
    merged_df = merged_df.merge(sat_times[["CPU_time"]], on="Solver", how="left", suffixes=("", "_SAT"))
    merged_df = merged_df.merge(unsat_times[["CPU_time"]], on="Solver", how="left", suffixes=("", "_UNSAT"))

    return merged_df, df_per_formula

def hypotesis_test(groups_sizes, clust_values):
    from scipy.stats import ks_2samp
    columns = ["Family", "Attribute", "Generator", "KS p-value"]
    tests_df = pd.DataFrame(columns=columns)

    orig_family_name = args.orig.strip(os.path.sep).split(os.path.sep)[-1]
    group_sizes_orig = groups_sizes[orig_family_name]
    clust_values_orig = clust_values[orig_family_name]

    for dist in args.generator_list:
        family_name = dist.strip(os.path.sep).split(os.path.sep)[-1]

        group_sizes_gen = groups_sizes[family_name]
        statistic, pvalue = ks_2samp(group_sizes_orig["group_sizes"], group_sizes_gen["group_sizes"])
        tests_df = tests_df.append(pd.DataFrame([[family_name, "Modularity group sizes", dist.strip("\\").strip("/").split("_")[-1], pvalue]], columns=columns))

        clust_values_gen = clust_values[family_name]
        statistic, pvalue = ks_2samp(clust_values_orig["clust_values"], clust_values_gen["clust_values"])
        tests_df = tests_df.append(pd.DataFrame([[family_name, "Clustering values", dist.strip("\\").strip("/").split("_")[-1], pvalue]], columns=columns))

    tests_df.to_csv(os.path.join(args.results, "test_comparison.csv"), index=False)

def analytical_comparison(df_results):
    analytical_df = pd.concat(df_results).reset_index(drop=True)
    table_vig, table_powerlaw = latex_table.gen_table(analytical_df)

    with open(os.path.join(args.results, "table_vig.tex"), "w") as f:
        f.write(table_vig)

    with open(os.path.join(args.results, "table_powerlaw.tex"), "w") as f:
        f.write(table_powerlaw)

def solvers_comparison(df_results, df_solvers):
    analytical_df = pd.concat(df_results).reset_index(drop=True)

    df_solvers_orig = df_solvers[0]
    df_solvers_orig["ranking"] = df_solvers_orig["CPU_time"].rank(method="first")
    df_solvers_orig["ranking_SAT"] = df_solvers_orig["CPU_time_SAT"].rank(method="first")
    df_solvers_orig["ranking_UNSAT"] = df_solvers_orig["CPU_time_UNSAT"].rank(method="first")

    total_formulas_orig = df_solvers_orig.iloc[0]["#_SAT"] + df_solvers_orig.iloc[0]["#_UNSAT"] + df_solvers_orig.iloc[0]["#_INDET"]
    df_solvers_orig["%_SAT"] = df_solvers_orig["#_SAT"] / total_formulas_orig * 100
    df_solvers_orig["%_UNSAT"] = df_solvers_orig["#_UNSAT"] / total_formulas_orig * 100
    df_solvers_orig["%_INDET"] = df_solvers_orig["#_INDET"] / total_formulas_orig * 100
    df_solvers_orig = df_solvers_orig.sort_values(by="Solver")
    df_solvers_orig.to_csv(os.path.join(args.results, f'{list(analytical_df["Family name"])[0]}_solvers.csv'))
    # print(df_solvers_orig)

    kendall_results = [1]
    kendall_results_sat = [1]
    kendall_results_unsat = [1]
    kendall_sat_pvalue = [0]
    kendall_unsat_pvalue = [0]
    mean_sat = [np.mean(np.array(df_solvers_orig["%_SAT"]))]
    mean_unsat = [np.mean(np.array(df_solvers_orig["%_UNSAT"]))]
    mean_indet = [np.mean(np.array(df_solvers_orig["%_INDET"]))]
    mean_cpu_time = [np.mean(np.array(df_solvers_orig["CPU_time"]))]

    for dist in range(1,len(df_solvers)):
        df_solvers_gen = df_solvers[dist]
        df_solvers_gen["ranking"] = df_solvers_gen["CPU_time"].rank(method="first")
        df_solvers_gen["ranking_SAT"] = df_solvers_gen["CPU_time_SAT"].rank(method="first")
        df_solvers_gen["ranking_UNSAT"] = df_solvers_gen["CPU_time_UNSAT"].rank(method="first")
        total_formulas_gen = df_solvers_gen.iloc[0]["#_SAT"] + df_solvers_gen.iloc[0]["#_UNSAT"] + df_solvers_gen.iloc[0]["#_INDET"]
        df_solvers_gen["%_SAT"] = df_solvers_gen["#_SAT"] / total_formulas_gen * 100
        df_solvers_gen["%_UNSAT"] = df_solvers_gen["#_UNSAT"] / total_formulas_gen * 100
        df_solvers_gen["%_INDET"] = df_solvers_gen["#_INDET"] / total_formulas_gen * 100
        mean_sat.append(np.mean(np.array(df_solvers_gen["%_SAT"])))
        mean_unsat.append(np.mean(np.array(df_solvers_gen["%_UNSAT"])))
        mean_indet.append(np.mean(np.array(df_solvers_gen["%_INDET"])))
        mean_cpu_time.append(np.mean(np.array(df_solvers_gen["CPU_time"])))

        df_solvers_gen = df_solvers_gen.sort_values(by="Solver")
        df_solvers_gen.to_csv(os.path.join(args.results, f'{list(analytical_df["Family name"])[dist]}_solvers.csv'))

        kendall_sat = kendalltau(df_solvers_orig["ranking_SAT"], df_solvers_gen["ranking_SAT"])
        kendall_unsat = kendalltau(df_solvers_orig["ranking_UNSAT"], df_solvers_gen["ranking_UNSAT"])

        print(df_solvers_orig["ranking_SAT"])
        print(df_solvers_gen["ranking_SAT"])


        kendall_results_sat.append(kendall_sat.correlation)
        kendall_sat_pvalue.append(kendall_sat.pvalue)
        kendall_results_unsat.append(kendall_unsat.correlation)
        kendall_unsat_pvalue.append(kendall_unsat.pvalue)

        print(kendall_sat_pvalue)
        print(kendall_unsat_pvalue)

    solver_comp = pd.DataFrame({"Family name":list(analytical_df["Family name"]),
                                "Kendall Coeff. (SAT)":kendall_results_sat, "p-value (SAT)":kendall_sat_pvalue,
                                "Kendall Coeff. (UNSAT)":kendall_results_unsat, "p-value (UNSAT)":kendall_unsat_pvalue,
                                "%_SAT (mean)": mean_sat, "%_UNSAT (mean)": mean_unsat, "%_TIMEOUT (mean)": mean_indet,
                                "CPU time (mean)":mean_cpu_time})

    print(solver_comp)

    solver_comp.to_excel(os.path.join(args.results, "solvers_table.xlsx"), index=False)

    table = latex_table.solvers_table(solver_comp)

    with open(os.path.join(args.results, "solvers_table.tex"), "w") as f:
        print(table)
        f.write(table)


df_results = []
df_per_formula_joined = []
df_solvers = []
groups_sizes = {}
clust_values = {}
alt_names = []
for dir_path in [args.orig] + args.generator_list:
    family_name = dir_path.strip(os.path.sep).split(os.path.sep)[-1]
    if dir_path != args.orig:
        alt_names.append(family_name)
    else:
        orig_name = family_name

    if not args.light:
        VIGs = {path: modularity.sat_to_VIG(os.path.join(dir_path, path)) for path in os.listdir(dir_path) if path[-4:] == ".cnf"}
    else:
        VIGs = [os.path.join(dir_path, path) for path in os.listdir(dir_path) if path[-4:] == ".cnf"]

    df_extracted_values = pd.DataFrame([family_name], columns = ["Family name"])
    df_per_formula = pd.DataFrame([path for path in os.listdir(dir_path) if path[-4:] == ".cnf"], columns=["Formula"])

    df_extracted_values, df_per_formula, groups_sizes_df = extract_mod(VIGs, family_name, df_extracted_values, df_per_formula)

    df_extracted_values, df_per_formula, clust_values_df = extract_clust(VIGs, family_name, df_extracted_values, df_per_formula)

    print(df_extracted_values)
    print(df_per_formula)

    del VIGs

    df_extracted_values = extract_scale_free(dir_path, df_extracted_values)

    if not args.ignore_solvers:
        df_solvers_i, df_per_formula = extract_solvers(dir_path, df_per_formula)

    df_results.append(df_extracted_values)
    df_per_formula_joined.append(df_per_formula)
    if not args.ignore_solvers:
        df_solvers.append(df_solvers_i)
        print(df_solvers)
    groups_sizes[family_name] = groups_sizes_df
    clust_values[family_name] = clust_values_df


plots = {}
for dir_path in [args.orig] + args.generator_list:
    family_name = dir_path.strip(os.path.sep).split(os.path.sep)[-1]

    with open(os.path.join(args.results, f"{family_name}-scale_free.plt")) as f:
        txt = f.readlines()

    plots[family_name] = txt

degree_dist.join_plots(plots, args.results, "scale_free_agg.png")


analytical_comparison(df_results)

if not args.ignore_solvers:
    solvers_comparison(df_results, df_solvers)
