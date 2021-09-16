import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", required=True)

args = parser.parse_args()

from pathlib import Path
path_res = Path(args.output)
path_res.mkdir(parents=True, exist_ok=True)

for form in os.listdir(args.input):
    if form[-4:] == ".cnf":
        result = subprocess.run([f'./SatELite_v1.0_linux {os.path.join(args.input, form)} {os.path.join(args.output, f"{form[:-4]}.processed.cnf")}'], shell=True, capture_output=True)
        print(result.returncode)