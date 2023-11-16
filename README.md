# get_exemplars_and_prep_complexes

Use to generate exemplars and then prep complexes for Shipra's PocketDruggability model

To generate exemplars use gen_exemplars.py. 
- This takes 3 inputs:
  - full folder path to location of models for which you want to generate exemplars (use pwd to get full file path)
  - number of chains for protein B: number of chains that are considered part of the second protein. If it is a two protein complex, put 1
  - interface distance: this will consider any atom on one chain within this distance to another chain for building the exemplars

- example command:
  - python use gen_exemplars.py /Users/mischlv/Downloads/practice_exemplar/ 1 12
 
- output:
  - this script will output all potnetial exemplars into the folder to which you directed the script  
 

To prep models to use in Shipra's PocketDruggability model use prep_files_for_shipra.py
- This takes 1 input:
  -  full folder path to location of models for which you want to generate exemplars (use pwd to get full file path)

- example command:
  - python prep_files_for_shipra.py /Users/mischlv/Downloads/practice_exemplar/
 
- output:
  - this script will generate a folder for the apo structures and place the apo structures in it
  - this script will generate a folder for the compelex structures and will place the file with the apo + exemplar file into the complex folder.   
