from abc import ABC, abstractmethod, abstractproperty
import subprocess
import os
import time

def remove_file(path, max_retries=5):
    for rt in range(max_retries):
        try:
            os.remove(path)
        except PermissionError as e:
            if rt <= max_retries - 1:
                time.sleep(0.5)
                continue
            else:
                raise e
        break

class Solver(ABC):
    @abstractmethod
    def solve(self, path, time_limit):
        pass

class Cadical(Solver):
    def __init__(self):
        self.solver_path = "solvers/bin/cadical"
        self.name = "Cadical"

    def solve(self, path, time_limit=-1):
        output_file = "result_cadical.txt"
        
        if time_limit != -1:
            time_str_opt = f"-t {time_limit}"
        else:
            time_str_opt = ""

        returned_val = subprocess.run([f'{self.solver_path} {time_str_opt} -w {output_file} {path}'], shell=True, capture_output=True)

        output_lines = returned_val.stdout.decode('utf-8').split("\n")
        for line in output_lines:
            if "total real time" in line:
                import re
                cpu_time = float(re.findall("\d+\.\d+", line)[0])

        with open(output_file) as f:
            file_result = f.readlines()[0].replace("s ", "").replace("c ", "").strip()

        remove_file(output_file)
            
        if file_result == "SATISFIABLE":
            result = "SAT"
        elif file_result == "UNSATISFIABLE":
            result = "UNSAT"
        elif file_result == "UNKNOWN":
            result = "INDET"
        else:
            raise ValueError("Not recognized result")

        return result, cpu_time


class Lingeling(Solver):
    def __init__(self):
        self.solver_path = "solvers/bin/lingeling"
        self.name = "Lingeling"

    def solve(self, path, time_limit=-1):
        if time_limit != -1:
            time_str_opt = f"-T {time_limit}"
        else:
            time_str_opt = ""

        returned_val = subprocess.run([f'{self.solver_path} {time_str_opt} {path}'], shell=True, capture_output=True)

        output_str = returned_val.stdout.decode('utf-8')
        output_lines = output_str.strip("\n").split("\n")
                       
        import re
        cpu_time = float(re.findall("\d+\.\d+", output_lines[-1])[0])

        if re.search("s SATISFIABLE", output_str):
            result = "SAT"
        elif re.search("s UNSATISFIABLE", output_str):
            result = "UNSAT"
        elif re.search("s UNKNOWN", output_str):
            result = "INDET"
        else:
            raise ValueError("Not recognized result")

        return result, cpu_time


class MinisatBased(Solver):
    @abstractmethod
    def __init__(self):
        self.solver_path = ""
        self.name = ""

    def parse_result_value(self, output: str):
        import re
        if re.search(r'\bSATISFIABLE\b', output):
            result = "SAT"
        elif re.search(r'\bUNSATISFIABLE\b', output):
            result = "UNSAT"
        elif re.search(r'\bINDETERMINATE\b', output):
            result = "INDET"
        else:
            raise ValueError("Not recognized result")
        
        return result

    def parse_cpu_time(self, output: str):
        output = output.strip('\n').split("\n")
        for line in output:
            if "CPU time" in line:
                import re
                cpu_time = float(re.findall("\d+\.\d+", line)[0])

        return cpu_time

    def parse_results(self, output):
        result = self.parse_result_value(output)
        cpu_time = self.parse_cpu_time(output)

        return result, cpu_time

    def solve(self, path, time_limit=-1):        
        if time_limit != -1:
            time_str_opt = f"-cpu-lim={time_limit}"
        else:
            time_str_opt = ""

        returned_val = subprocess.run([f'{self.solver_path} {time_str_opt} {path}'], shell=True, capture_output=True)
        output = returned_val.stdout.decode('utf-8')

        result = self.parse_results(output)

        return result

        

class Glucose(MinisatBased):
    def __init__(self):
        self.solver_path = "solvers/bin/glucose"
        self.name = "Glucose"


class MapleSAT(MinisatBased):
    def __init__(self):
        self.solver_path = "solvers/bin/maplesat"
        self.name = "MapleSAT"
        

class MapleLCM(MinisatBased):
    def __init__(self):
        self.solver_path = "solvers/bin/MapleLCMDistChrBt-DL-v3"
        self.name = "MapleLCMDiscChronoBT-DL-v3"

    def parse_result_value(self, output: str):
        import re
        if re.search(r'\bSATISFIABLE\b', output):
            result = "SAT"
        elif re.search(r'\bUNSATISFIABLE\b', output):
            result = "UNSAT"
        else:
            raise ValueError("Not recognized result")
        
        return result

    def solve(self, path, time_limit=-1):
        if time_limit != -1:
            time_str_opt = f"timeout {time_limit}"
        else:
            time_str_opt = ""

        returned_val = subprocess.run([f'{time_str_opt} {self.solver_path} {path}'], shell=True, capture_output=True)
        output = returned_val.stdout.decode('utf-8')


        if returned_val.returncode == 124:
            result = "INDET"
            cpu_time = float(time_limit)
        else:
            result = self.parse_result_value(output)
            cpu_time = self.parse_cpu_time(output)

        return result, cpu_time

if __name__=="__main__":
    print("####################### GLUCOSE #######################")

    glc = Glucose()

    print("SAT: ", glc.solve("data/desgen/gss-16-s100.cnf", 100))
    print("UNSAT: ", glc.solve("data/ibm/SAT_dat.k45.cnf", 100))
    print("UNKNOWN: ", glc.solve("data/anbulagan/dated-10-13-u.cnf", 20))

    print("####################### MAPLESAT #######################")

    glc = MapleSAT()

    print("SAT: ", glc.solve("data/desgen/gss-16-s100.cnf", 100))
    print("UNSAT: ", glc.solve("data/ibm/SAT_dat.k45.cnf", 100))
    print("UNKNOWN: ", glc.solve("data/anbulagan/dated-10-13-u.cnf", 20))

    print("####################### MAPLELCM #######################")

    glc = MapleLCM()

    print("SAT: ", glc.solve("data/desgen/gss-16-s100.cnf", 100))
    print("UNSAT: ", glc.solve("data/ibm/SAT_dat.k45.cnf", 100))
    print("UNKNOWN: ", glc.solve("data/anbulagan/dated-10-13-u.cnf", 20))

    print("####################### Lingeling #######################")

    glc = Lingeling()

    print("SAT: ", glc.solve("data/desgen/gss-16-s100.cnf", 100))
    print("UNSAT: ", glc.solve("data/ibm/SAT_dat.k45.cnf", 100))
    print("UNKNOWN: ", glc.solve("data/anbulagan/dated-10-13-u.cnf", 20))

    print("####################### Cadical #######################")

    glc = Cadical()

    print("SAT: ", glc.solve("data/desgen/gss-16-s100.cnf", 100))
    print("UNSAT: ", glc.solve("data/ibm/SAT_dat.k45.cnf", 100))
    print("UNKNOWN: ", glc.solve("data/anbulagan/dated-10-13-u.cnf", 20))

