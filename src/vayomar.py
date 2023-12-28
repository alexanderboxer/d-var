'''
vayomer vs vayomar
'''
#==================================================
# Imports
#==================================================
import os 
import git 
import pandas as pd

#==================================================
# Paths
#==================================================
def get_project_root():
    return git.Repo('.', search_parent_directories=True).working_tree_dir

project_root = get_project_root()
source_directory = os.path.join(project_root,'wordframe')
source_filename = 'words.csv'
source_filepath = os.path.join(source_directory, source_filename)

#==================================================
# Load dataframe
#==================================================
df = pd.read_csv(source_filepath)

#==================================================
# Slice and dice
#==================================================
df2 = df[df.d0 == 'ויאמר']
df3 = df[df.d1 == 'וַיֹּאמַר']

