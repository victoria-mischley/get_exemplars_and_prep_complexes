import pandas as pd
import argparse
from pathlib import Path
import numpy as np
from biopandas.pdb import PandasPdb
import copy

def args():
    parser = argparse.ArgumentParser()
    # Add command line arguments
    parser.add_argument('file_path', type=str, help='path to location of AF folder output')
    parser.add_argument('num_chains_protein_B', type=str, help='number of chains of the last protein')
    parser.add_argument('interface_cutoff', type=str, help='distance that defines the interface')
    # Parse the command line arguments
    args = parser.parse_args()

    return args


def get_if_residues(file_path, num_chains_protein_B, interface_cutoff):
    results = []
    AF = PandasPdb().read_pdb(str(file_path))
    print(file_path)
    chains_AF = []
    for chain_ID in AF.df['ATOM']['chain_id'].unique():
        chains_AF.append(chain_ID)
    
    total_number_chains = len(chains_AF)
    num_chains_protein_A = total_number_chains - int(num_chains_protein_B)
    chains_AF_A = chains_AF[:num_chains_protein_A]
    chains_AF_B = chains_AF[num_chains_protein_A:]
    
    for ind in AF.df['ATOM']['chain_id'].index:
        current_chain_ID = AF.df['ATOM']['chain_id'][ind]
        if current_chain_ID in chains_AF_A:
            AF.df['ATOM'].at[ind, 'chain_id'] = 'A'
        else:
            AF.df['ATOM'].at[ind, 'chain_id'] = 'B'
        
    AF_chainA = AF.df['ATOM'][AF.df['ATOM']['chain_id'] == 'A']
    AF_chainB = AF.df['ATOM'][AF.df['ATOM']['chain_id'] == 'B']
    
    AF_chainA_CB = AF_chainA.loc[(AF_chainA['atom_name'] == 'CB') | ((AF_chainA['residue_name'] == 'GLY') & (AF_chainA['atom_name'] == 'CA'))]
    AF_chainB_CB = AF_chainB.loc[(AF_chainB['atom_name'] == 'CB') | ((AF_chainB['residue_name'] == 'GLY') & (AF_chainB['atom_name'] == 'CA'))]
    
    for ind in AF_chainA_CB.index:
        X_coord_A = AF_chainA_CB['x_coord'][ind]
        Y_coord_A = AF_chainA_CB['y_coord'][ind]
        Z_coord_A = AF_chainA_CB['z_coord'][ind]
        plDDt_A = AF_chainA_CB['b_factor'][ind]
        resname_A = AF_chainA_CB['residue_name'][ind]
        res_number_A = AF_chainA_CB['residue_number'][ind]
        for B_ind in AF_chainB_CB.index:
            X_coord_B = AF_chainB_CB['x_coord'][B_ind]
            Y_coord_B = AF_chainB_CB['y_coord'][B_ind]
            Z_coord_B = AF_chainB_CB['z_coord'][B_ind]
            plDDt_B = AF_chainB_CB['b_factor'][B_ind]
            resname_B = AF_chainB_CB['residue_name'][B_ind]
            res_number_B = AF_chainB_CB['residue_number'][B_ind]
            distance = np.sqrt((X_coord_A - X_coord_B) **2 + (Y_coord_A - Y_coord_B) **2 + (Z_coord_A - Z_coord_B) **2)
            if distance <= int(interface_cutoff):
                results.append({'resname_A': resname_A, 'res_numberA': res_number_A, 'resname_B': resname_B, 'res_numberB': res_number_B, 'distance': distance})
    results_df = pd.DataFrame(results)
    print(results_df)

    return results_df

def get_unique_res(file_path, num_chains_protein_B, interface_cutoff):
    interface_df = get_if_residues(file_path, num_chains_protein_B, interface_cutoff)
    chain_A_unique_res = set()
    chain_B_unique_res = set()
    for ind in interface_df.index:
        chain_A_res = interface_df['res_numberA'][ind]
        chain_A_unique_res.add(chain_A_res)
        chain_B_res = interface_df['res_numberB'][ind]
        chain_B_unique_res.add(chain_B_res)
    return chain_A_unique_res, chain_B_unique_res

def get_res_pairs(file_path, num_chains_protein_B, interface_cutoff):
    chain_A_unique_res, chain_B_unique_res = get_unique_res(file_path, num_chains_protein_B, interface_cutoff)
    chain_A_unique_res_list = list(chain_A_unique_res)
    chain_B_unique_res_list = list(chain_B_unique_res)
    res_pairs = []
    for val in chain_A_unique_res_list:
        chainAres = val
        for ind in chain_B_unique_res_list:
            chainBres = ind
            res_pairs.append({'chainAres': chainAres, 'chainBres': chainBres})
    res_pairs_df = pd.DataFrame(res_pairs)

    return res_pairs_df

def get_exemplar_command(file_path, num_chains_protein_B, interface_cutoff):
    res_pairs_df  = get_res_pairs(file_path, num_chains_protein_B, interface_cutoff)
    file_path_path = Path(file_path)
    file_name = file_path_path.name
    command_list = []
    for ind in res_pairs_df.index:
        chainAres = res_pairs_df['chainAres'][ind]
        chainBres = res_pairs_df['chainBres'][ind]
        command = f"~/Rosetta/main/source/bin/make_exemplar.default.macosclangrelease -database ~/Rosetta/main/database/ -s {file_name} -pocket_num_angles 100 -pocket_psp -pocket_grid_size 10 -pocket_max_spacing 12 -central_relax_pdb_num {chainAres}:A,{chainBres}:B -pocket_filter_by_exemplar -pocket_static_grid -pocket_limit_exemplar_color -pocket_dump_exemplars -min_atoms 1 -max_atoms 65"
        command_list.append(command)
    return command_list



if __name__ == '__main__':
    args = args()
    # interface_df = get_if_residues(args.file_path, args.num_chains_protein_B, args.interface_cutoff)
    # chain_A_unique_res, chain_B_unique_res = get_unique_res(args.file_path, args.num_chains_protein_B, args.interface_cutoff)
    # print(chain_A_unique_res)
    # res_pairs_df = get_res_pairs(args.file_path, args.num_chains_protein_B, args.interface_cutoff)
    # print(res_pairs_df)
    command_list = get_exemplar_command(args.file_path, args.num_chains_protein_B, args.interface_cutoff)
    print(len(command_list))
    print(command_list[1])

