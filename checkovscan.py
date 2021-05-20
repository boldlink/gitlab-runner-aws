# Simple script to extract the checkov scan skip codes
import argparse
import subprocess
from pathlib import Path
import os

parser = argparse.ArgumentParser(description='Checkov scan wrapper')
parser.add_argument('--file', type=Path, dest='file', help='Path to file with skip codes')
parser.add_argument('--path', dest='path', help='Path with the files to scan')
args = parser.parse_args()

path = args.path
file = args.file

def codeList(path):
    path = os.path.abspath(path)
    
    with open(file, 'r') as f:
        skip_dic = dict(x.rstrip().split(None, 1) for x in f)

    key_list = []
    for key in skip_dic.keys():
        key_list.append(key)
        skip_codes = []
        skip_codes = ','.join([div.replace(":", "") for div in key_list])
    
    return skip_codes

try:
    # dpath = os.path.abspath(args.path)
    cmd = ["checkov", "-d", path, "--skip-check", codeList(path)]
    print(f'Executing checkov command: {cmd}')
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

except Exception as e:
    print(f"Exception: {e}")