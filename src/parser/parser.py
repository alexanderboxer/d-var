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
def get_project_root():
    return git.Repo('.', search_parent_directories=True).working_tree_dir

project_root = get_project_root()
source_directory = os.path.join(project_root,'sourcetexts')
target_directory = os.path.join(project_root, 'wordframe')

#==================================================
# Function: chapterlist_to_dataframe
#==================================================
def chapterlist_to_dataframe(chapterlist):
    wordlist, idxlist = list(), list()
    for chapter_idx, chapter in enumerate(chapterlist):
        for verse_idx, verse in enumerate(chapter):
             wordlist += verse.split()
             idxlist += ['{}.{}.{}'.format(1 + chapter_idx, 1 + verse_idx, 1 + k) for k in range(len(verse.split()))]
    df = pd.DataFrame(zip(idxlist, wordlist), columns = ['idx','mot']).set_index('idx')
    return df


#==================================================
# Read
#==================================================
for book_idx, bookname in enumerate(sorted(os.listdir(source_directory))[:1]):
    bookpath = os.path.join(source_directory, bookname)
    book_dataframe_list = list()
    for filename in sorted(os.listdir(bookpath)):
        with open(os.path.join(bookpath, filename)) as f:
            chapterlist = json.load(f)['text']
        book_dataframe_list.append(chapterlist_to_dataframe(chapterlist))
    book_df = book_dataframe_list[0].rename(columns={'mot':'mot0'})
    for i, dataframe in enumerate(book_dataframe_list[1:]):
        book_df = book_df.join(dataframe.rename(columns={'mot':'mot{}'.format(i+1)}), how='outer')

book_df['cap'] = [float(k.split('.')[0]) for k in book_df.index]
book_df['verse'] = [float(k.split('.')[1]) for k in book_df.index]
book_df['word'] = [float(k.split('.')[-1]) for k in book_df.index]

book_df = book_df.sort_values(['cap','verse','word']).drop(['cap','verse','word'], axis = 1)

#==================================================
# Export
#==================================================
target_filepath = os.path.join(target_directory, 'words.csv')
book_df.to_csv(target_filepath)

