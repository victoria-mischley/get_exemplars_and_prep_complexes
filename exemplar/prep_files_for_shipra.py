import pandas as pd
import argparse
from pathlib import Path
import get_interface_residues
import os
import shutil

def args():
    parser = argparse.ArgumentParser()
    # Add command line arguments
    parser.add_argument('folder_path', type=str, help='path to location of AF folder output')
    # Parse the command line arguments
    args = parser.parse_args()

    return args

def copy_files(folder_path):
    folder_path_path = Path(folder_path)
    if not os.path.exists(f"{folder_path_path}/apo/"):
        os.mkdir(f"{folder_path_path}/apo/")
    for file in folder_path_path.iterdir():
        if file.is_file():
            file_name = file.name
            pdb_count = file_name.count(".pdb")
            if pdb_count == 1:
                src  = f"{folder_path_path}/{file_name}"
                dct = f"{folder_path_path}/apo/{file_name}"
                shutil.copy(src, dct)

def make_complexes(folder_path):
    folder_path_path = Path(folder_path)
    if not os.path.exists(f"{folder_path_path}/complexes/"):
        os.mkdir(f"{folder_path_path}/complexes/")
    for file in folder_path_path.iterdir():
        if file.is_file():
            file_name = file.name
            pdb_count = file_name.count(".pdb")
            if pdb_count == 2:
                apo_file_name = file_name.split(".pdb")[0]
                apo_file_path = f"{folder_path_path}/apo/{apo_file_name}.pdb"
                exemplar_file_path = file
                complex_file_path = f"{folder_path_path}/complexes/{apo_file_name}_{exemplar_file_path}_Complex.pdb"
                with open(apo_file_path, 'r') as f1:
                    apo_data = f1.read()
                with open(exemplar_file_path) as f2:
                    exemplar_data = f2.read()
                with open(complex_file_path, 'w') as f3:
                    f3.write(apo_data + "\n" + exemplar_data)

if __name__ == '__main__':
    args = args()
    copy_files(args.folder_path)
    make_complexes(args.folder_path)
