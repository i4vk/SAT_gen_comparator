def get_error(orig_value, new_value):
    diff = abs(new_value-orig_value)
    error = (diff/orig_value) * 100
    return round(error)

def gen_table_VIG(df):
    header = '''\\begin{table}[]
                \\begin{tabular}{|c|c|c|c|}
                \hline
                \multirow{2}{*}{\\textbf{Generator}} & \multicolumn{3}{c|}{\\textbf{VIG}} \\\\ \cline{2-4} 
                & \\textbf{Modularity} & \\textbf{\# communities} & \\textbf{Clustering Coef} \\\\ \hline \n'''
# papaya                     &            &                &                 &                   &        &       &        \\
#                            &            &                &                 &                   &        &       &        \\
#                            &            &                &                 &                   &        &       &       
    
    end = "\end{tabular} \end{table}"

    latex_rows = ""

    for index, row in df.iterrows():
        if index == 0:
            latex_rows += f'''{row["Family name"].replace("_", " ")} & {round(row["mod_mean"], 2)} $\pm$ {round(row["mod_std"], 2)} 
                            & {round(row["#comm_mean"], 2)} $\pm$ {round(row["#comm_std"], 2)} 
                            & {round(row["clust_mean"], 2)} $\pm$ {round(row["clust_std"], 2)} \\\\ \hline \hline \n'''
        else:
            latex_rows += f'''{row["Family name"].replace("_", " ")} & {round(row["mod_mean"], 2)} $\pm$ {round(row["mod_std"], 2)} ({get_error(df.iloc[0]["mod_mean"], row["mod_mean"])} $\%$)
                            & {round(row["#comm_mean"], 2)} $\pm$ {round(row["#comm_std"], 2)} ({get_error(df.iloc[0]["#comm_mean"], row["#comm_mean"])} $\%$)
                            & {round(row["clust_mean"], 2)} $\pm$ {round(row["clust_std"], 2)} ({get_error(df.iloc[0]["clust_mean"], row["clust_mean"])} $\%$) \\\\ \hline \n'''

            

    table = header + latex_rows + end
    return table

def gen_table_powerlaw(df):
    header = '''\\begin{table}[]
                \\begin{tabular}{|c|c|c|c|}
                \hline
                \multirow{2}{*}{\\textbf{Generator}} & \multicolumn{3}{c|}{\\textbf{Powerlaw}} \\\\ \cline{2-4} 
                & \\textbf{Variable $\\alpha$} & \\textbf{k\_min} & \\textbf{error} \\\\ \hline \n'''
# papaya                     &            &                &                 &                   &        &       &        \\
#                            &            &                &                 &                   &        &       &        \\
#                            &            &                &                 &                   &        &       &       
    
    end = "\end{tabular} \end{table}"

    latex_rows = ""

    for index, row in df.iterrows():
        if index == 0:
            latex_rows += f'''{row["Family name"].replace("_", " ")} & {round(row["powerlaw-alpha"], 2)} & {round(row["powerlaw-k_min"], 2)} 
                            & {round(row["powerlaw-error"], 2)} \\\\ \hline \hline \n'''
        else:
            latex_rows += f'''{row["Family name"].replace("_", " ")} & {round(row["powerlaw-alpha"], 2)} ({get_error(df.iloc[0]["powerlaw-alpha"], row["powerlaw-alpha"])} $\%$) 
                            & {round(row["powerlaw-k_min"], 2)} ({get_error(df.iloc[0]["powerlaw-k_min"], row["powerlaw-k_min"])} $\%$)
                            & {round(row["powerlaw-error"], 2)} \\\\ \hline \n'''

            

    table = header + latex_rows + end
    return table

# def gen_table_powerlaw(df):
#     header = '''\\begin{table}[]
#                 \\begin{tabular}{|c|c|c|c|c|}
#                 \hline
#                 \multirow{2}{*}{\\textbf{Generator}} & \multicolumn{4}{c|}{\\textbf{Powerlaw}} \\\\ \cline{2-5} 
#                 & \\textbf{Variable $\\alpha$} & \\textbf{k\_min} & \\textbf{error} & \\textbf{k\_err} \\\\ \hline \n'''
# # papaya                     &            &                &                 &                   &        &       &        \\
# #                            &            &                &                 &                   &        &       &        \\
# #                            &            &                &                 &                   &        &       &       
    
#     end = "\end{tabular} \end{table}"

#     latex_rows = ""

#     for index, row in df.iterrows():
#         if index == 0:
#             latex_rows += f'''{row["Family name"].replace("_", " ")} & {round(row["powerlaw-alpha"], 2)} & {round(row["powerlaw-k_min"], 2)} 
#                             & {round(row["powerlaw-error"], 2)} & {round(row["powerlaw-k_err"], 2)} \\\\ \hline \hline \n'''
#         else:
#             latex_rows += f'''{row["Family name"].replace("_", " ")} & {round(row["powerlaw-alpha"], 2)} ({get_error(df.iloc[0]["powerlaw-alpha"], row["powerlaw-alpha"])} $\%$) 
#                             & {round(row["powerlaw-k_min"], 2)} ({get_error(df.iloc[0]["powerlaw-k_min"], row["powerlaw-k_min"])} $\%$)
#                             & {round(row["powerlaw-error"], 2)} ({get_error(df.iloc[0]["powerlaw-error"], row["powerlaw-error"])} $\%$)
#                             & {round(row["powerlaw-k_err"], 2)} ({get_error(df.iloc[0]["powerlaw-k_err"], row["powerlaw-k_err"])} $\%$) \\\\ \hline \n'''

            

#     table = header + latex_rows + end
#     return table

def gen_table(df):
    table_vig = gen_table_VIG(df)
    table_powerlaw = gen_table_powerlaw(df)

    return table_vig, table_powerlaw


# def gen_table(df):
#     header = '''\\begin{table}[]
# \\begin{tabular}{|c|c|c|c|c|c|c|c|}
# \hline
# \multirow{2}{*}{\\textbf{Generator}} &
#   \multicolumn{3}{c|}{\\textbf{VIG}} &
#   \multicolumn{4}{c|}{\\textbf{Powerlaw}} \\\\ \cline{2-8} 
#  &
#   \\textbf{Modularity} &
#   \\textbf{\# communities} &
#   \\textbf{Clustering Coef} &
#   \\textbf{Variable $\\alpha$} &
#   \\textbf{k\_min} &
#   \\textbf{error} &
#   \\textbf{k\_err} \\\\ \hline \n'''
# # papaya                     &            &                &                 &                   &        &       &        \\
# #                            &            &                &                 &                   &        &       &        \\
# #                            &            &                &                 &                   &        &       &       
    
#     end = "\end{tabular} \end{table}"

#     latex_rows = ""

#     for index, row in df.iterrows():
#         if index == 0:
#             latex_rows += f'''{row["Family name"].replace("_", " ")} & {round(row["mod_mean"], 2)} $\pm$ {round(row["mod_std"], 2)} 
#                             & {round(row["#comm_mean"], 2)} $\pm$ {round(row["#comm_std"], 2)} 
#                             & {round(row["clust_mean"], 2)} $\pm$ {round(row["clust_std"], 2)}
#                             & {round(row["powerlaw-alpha"], 2)} & {round(row["powerlaw-k_min"], 2)} 
#                             & {round(row["powerlaw-error"], 2)} & {round(row["powerlaw-k_err"], 2)} \\\\ \hline \n'''
#         else:
#             latex_rows += f'''{row["Family name"].replace("_", " ")} & {round(row["mod_mean"], 2)} $\pm$ {round(row["mod_std"], 2)} ({get_error(df.iloc[0]["mod_mean"], row["mod_mean"])} $\%$)
#                             & {round(row["#comm_mean"], 2)} $\pm$ {round(row["#comm_std"], 2)} ({get_error(df.iloc[0]["#comm_mean"], row["#comm_mean"])} $\%$)
#                             & {round(row["clust_mean"], 2)} $\pm$ {round(row["clust_std"], 2)} ({get_error(df.iloc[0]["clust_mean"], row["clust_mean"])} $\%$)
#                             & {round(row["powerlaw-alpha"], 2)} ({get_error(df.iloc[0]["powerlaw-alpha"], row["powerlaw-alpha"])} $\%$) 
#                             & {round(row["powerlaw-k_min"], 2)} ({get_error(df.iloc[0]["powerlaw-k_min"], row["powerlaw-k_min"])} $\%$)
#                             & {round(row["powerlaw-error"], 2)} ({get_error(df.iloc[0]["powerlaw-error"], row["powerlaw-error"])} $\%$)
#                             & {round(row["powerlaw-k_err"], 2)} ({get_error(df.iloc[0]["powerlaw-k_err"], row["powerlaw-k_err"])} $\%$) \\\\ \hline \n'''

            

#     table = header + latex_rows + end
#     return table


def solvers_table(df):
    header = '''\\begin{table}[]
\\begin{tabular}{|c|cccccc|}
\hline
\multirow{2}{*}{\\textbf{Generator}} & \multicolumn{6}{c|}{\\textbf{SAT Solvers}} \\\\ \cline{2-7} 
 & \multicolumn{1}{c|}{\\textbf{\\begin{tabular}[c]{@{}c@{}}$\\tau$ SAT\\\\ (p-value)\end{tabular}}} & \multicolumn{1}{c|}{\\textbf{\\begin{tabular}[c]{@{}c@{}}$\\tau$ UNSAT\\\\ (p-value)\end{tabular}}} & \multicolumn{1}{c|}{\\textbf{\%SAT}} & \multicolumn{1}{c|}{\\textbf{\%UNSAT}} & \multicolumn{1}{c|}{\\textbf{\%TIMEOUT}} & \\textbf{\\begin{tabular}[c]{@{}c@{}}CPU\\\\ time\end{tabular}} \\\\ \hline \n'''

    end = "\end{tabular} \end{table}"

    latex_rows = ""

    for index, row in df.iterrows():
        if index == 0:
            latex_rows += f'''{row["Family name"].replace("_", " ")} & - & - & {round(row["%_SAT (mean)"], 1)} 
                            & {round(row["%_UNSAT (mean)"], 1)} & {round(row["%_TIMEOUT (mean)"], 1)} & {round(row["CPU time (mean)"], 2)} \\\\ \hline \hline \n'''
        else:
            latex_rows += f'''{row["Family name"].replace("_", " ")}
                            & {round(row["Kendall Coeff. (SAT)"], 2)} ({round(row["p-value (SAT)"], 2)})
                            & {round(row["Kendall Coeff. (UNSAT)"], 2)} ({round(row["p-value (UNSAT)"], 2)})
                            & {round(row["%_SAT (mean)"], 1)} 
                            & {round(row["%_UNSAT (mean)"], 1)} 
                            & {round(row["%_TIMEOUT (mean)"], 1)}
                            & {round(row["CPU time (mean)"], 2)} \\\\ \hline \n'''

            

    table = header + latex_rows + end
    return table

# def solvers_table(df):
#     header = '''\\begin{table}[]
# \\begin{tabular}{|c|c|c|c|c|c|c|c|c|}
# 	\hline
# 	\multirow{2}{*}{\\textbf{Generator}} & \multicolumn{5}{c|}{\\textbf{SAT Solvers}} \\\\ \cline{2-9} 
# 	& \\textbf{Kendall SAT} & \\textbf{p-value (SAT)} & \\textbf{Kendall UNSAT} & \\textbf{p-value (UNSAT)} & \\textbf{\%SAT} & \\textbf{\%UNSAT} & \\textbf{\%TIMEOUT} & \\textbf{CPU time} \\\\ \hline \n'''

#     end = "\end{tabular} \end{table}"

#     latex_rows = ""

#     for index, row in df.iterrows():
#         if index == 0:
#             latex_rows += f'''{row["Family name"].replace("_", " ")} & - & - & - & {round(row["%_SAT (mean)"], 1)} 
#                             & {round(row["%_UNSAT (mean)"], 1)} & {round(row["%_TIMEOUT (mean)"], 1)} & {round(row["CPU time (mean)"], 2)} \\\\ \hline \hline \n'''
#         else:
#             latex_rows += f'''{row["Family name"].replace("_", " ")}
#                             & {round(row["Kendall Coeff. (SAT)"], 2)}
#                             & {round(row["p-value (SAT)"], 2)}
#                             & {round(row["Kendall Coeff. (UNSAT)"], 2)}
#                             & {round(row["p-value (UNSAT)"], 2)}
#                             & {round(row["%_SAT (mean)"], 1)} 
#                             & {round(row["%_UNSAT (mean)"], 1)} 
#                             & {round(row["%_TIMEOUT (mean)"], 1)}
#                             & {round(row["CPU time (mean)"], 2)} \\\\ \hline \n'''

            

#     table = header + latex_rows + end
#     return table
