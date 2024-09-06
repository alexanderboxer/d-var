'''
parse sourcetexts
'''
#==================================================
# Imports
#==================================================
import os 
import git 
import json
import pandas as pd

#==================================================
# Paths
#==================================================
project_root = git.Repo('.', search_parent_directories=True).working_tree_dir
wordframe_filepath = os.path.join(project_root,'wordframe','words.csv') 
target_directory = os.path.join(project_root, 'json')

#==================================================
# Load wordframe
#==================================================
df0 = pd.read_csv(wordframe_filepath)

#==================================================
# Subset
#==================================================
df = df0[df0.idx.apply(lambda x: x[:6]=='1.1.1.')] 

#==================================================
# Export to individual json files
#==================================================
words_jsonlist = df.to_json(orient='records', lines=True, force_ascii=False).split('\n')[:-1]

for word_json in words_jsonlist:
    word_dict = json.loads(word_json)
    target_filename = word_dict['idx'] + '.json'
    target_filepath = os.path.join(target_directory, target_filename)
    with open(target_filepath, 'w') as f:
        json.dump(word_dict, f, ensure_ascii=False)
