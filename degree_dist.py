from ntpath import join
import platform
import subprocess
import os
import time
import shutil

def clear_auxfiles(source_dir, max_retries = 5):
    if not os.path.isdir(source_dir):
        raise ValueError("Source must be a directory")

    for f in os.listdir(source_dir):
        if f[-4:] != ".cnf" and f[-4:] != ".png":
            for rt in range(max_retries):
                try:
                    os.remove(os.path.join(source_dir,f))
                except PermissionError as e:
                    if rt <= max_retries - 1:
                        time.sleep(0.5)
                        continue
                    else:
                        raise e
                break

def degree_dist(source, result_path):
    if os.path.isdir(source):
        if os.listdir(source)[0][-4:] == ".cnf":
            family = True
            family_name = source.strip(os.path.sep).split(os.path.sep)[-1]
        else:
            raise TypeError("Source must be a CNF file or a directory containing CNF files")
    else:
        if source[-4:] == ".cnf":
            family = False
            _, formula_name = os.path.split(source)
        else:
            raise TypeError("Source must be a CNF file or a directory containing CNF files")
            
    if platform.system() != "Linux":
        raise NotImplementedError("Only working over Linux systems.")

    
    if family == False:
        # os.chdir("GraphFeatures")
        # result = subprocess.run(["./features_s", "-1", "-a", os.path.join("..", source)])
        result = subprocess.run([f'GraphFeatures/features_s -1 -t {source+".alphavar"} -l {source+".alphavar.out"} \
                 -k {source+".alphavar.int"} -g {source+".alphavar.plt"} {source}'], shell=True, capture_output=True)
        # print(result)
        if result.returncode != 0:
            raise RuntimeError("Error extracting degree distribution features")
        # os.chdir("..")

        result_plot = subprocess.run(["gnuplot", f'{source+".alphavar.plt"}'])
        if result_plot.returncode != 0:
            raise RuntimeError("Error plotting degree distribution")

        with open(f'{source+".alphavar.out"}', "r") as results_f:
            output = results_f.readlines()
            powerlaw = True
            import re
            for line in output:
                if "EXPONENTIAL" in line:
                    powerlaw = False

                if powerlaw and "alpha" in line:
                    alpha = float(re.findall("\d+\.\d+", line)[0])
                if powerlaw and "min" in line:
                    kmin = int(re.findall("\d+", line)[0])
                if powerlaw and "error" in line:
                    error, k_err = re.findall(r"\d+.\d+|\d+", line)
                    error = float(error)
                    k_err = int(k_err)

        dir_path = os.path.join(*source.split(os.sep)[:-1])

    else:
        dir_path = source

        for cnf in os.listdir(source):
            if cnf[-4:] == ".cnf":
                result = subprocess.run([f'GraphFeatures/features_s -1 -t {os.path.join(source, cnf+".alphavar")} -l {os.path.join(source, cnf+".alphavar.out")} \
                 -k {os.path.join(source, cnf+".alphavar.int")} -g {os.path.join(source, cnf+".alphavar.plt")} {os.path.join(source, cnf)}'], shell=True, capture_output=True)
                 
                if result.returncode != 0:
                    raise RuntimeError(f"Error extracting degree distribution features of {os.path.join(source,cnf)} file")


        cwd = os.getcwd()
        os.chdir(source)
        result_concat = subprocess.run(['for i in `find . -name "*.alphavar"`;do cat $i >> kk; done'], shell=True)
        os.chdir(os.path.join(cwd, "GraphFeatures"))
        result_moslikely = subprocess.run([f"./mostlikely -f {os.path.join(cwd, source, 'kk')} -m 10 -p {os.path.join(cwd, source, 'kk.plt')} -i {os.path.join(cwd, source, 'kk.int')} -o {os.path.join(cwd, source, 'kk.out')}"], shell=True, capture_output=True)
        # print(result_moslikely)
        os.chdir(cwd)
        result_plot = subprocess.run(["gnuplot", f'{os.path.join(source, "kk.plt")}'])
        if result_plot.returncode != 0:
            raise RuntimeError("Error plotting degree distribution")

        with open(os.path.join(cwd, source, 'kk.out'), "r") as results_f:
            output = results_f.readlines()
            powerlaw = True
            import re
            for line in output:
                if "EXPONENTIAL" in line:
                    powerlaw = False

                if powerlaw and "alpha" in line:
                    alpha = float(re.findall("\d+\.\d+", line)[0])
                if powerlaw and "min" in line:
                    kmin = int(re.findall("\d+", line)[0])
                if powerlaw and "error" in line:
                    error, k_err = re.findall(r"\d+.\d+|\d+", line)
                    error = float(error)
                    k_err = int(k_err)


                # result_plt = subprocess.run(["gnuplot", f"{os.path.join(source, cnf)}.alphavar.plt"])

    if family:
        shutil.move(os.path.join(dir_path, "kk.png"), os.path.join(result_path, f"{family_name}-scale_free.png"))
    else:
        shutil.move(os.path.join(dir_path, f"{formula_name}.alphavar.png"), os.path.join(result_path, f"{formula_name}-scale_free.png"))
    clear_auxfiles(dir_path)

    return alpha, kmin, error, k_err

        

if __name__=="__main__":

    for dir in os.listdir("data"):
        print(os.path.join("data", dir))
        degree_dist(os.path.join("data", dir), "results")

    # degree_dist("data/prueba/countbitsarray02_32.cnf", "results")

    