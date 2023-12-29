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
    idxlist, wordlist, maqaflist, paseqlist, breaklist = list(), list(), list(), list(), list()
    for chapter_idx, verses in enumerate(chapterlist):
        for verse_idx, verse in enumerate(verses):
            word_tuplelist = list()
            maqaf_clusters = verse.split()
            for cluster in maqaf_clusters:
                cluster_elements = cluster.split('־')
                word_tuplelist += [(k[0],k[1]+1,k[2]) for k in zip(cluster_elements, range(len(cluster_elements)), [len(cluster_elements)] * len(cluster_elements))]
            notpaseq = [True if k[0] != '׀' else False for k in word_tuplelist]
            notbreak = [True if '(' not in k[0] else False for k in word_tuplelist]
            keepers = [bool(k[0] * k[1]) for k in zip(notpaseq, notbreak)]
            paseq = [not(k) for k in notpaseq[1:]] + [False]
            breaks = [k[0][0] if not(k[1]) else None for k in zip(word_tuplelist, notbreak)][1:] + [None] 
            word_tuplelist = [(k[0] + (k[1],) + (k[2],) + (k[3],)) for k in zip(word_tuplelist, paseq, breaks, keepers)]
            word_tuplelist = [k[:-1] for k in word_tuplelist if k[-1] == True]
            wordlist += [k[0] for k in word_tuplelist]
            maqaflist += [(k[1], k[2]) if k[2] > 1 else None for k in word_tuplelist]
            paseqlist += [k[3] for k in word_tuplelist]
            breaklist += [k[4] for k in word_tuplelist]
            idxlist += ['{}.{}.{}'.format(1 + chapter_idx, 1 + verse_idx, 1 + k) for k in range(len(word_tuplelist))]
        
    df = pd.DataFrame(zip(idxlist, wordlist, maqaflist, paseqlist, breaklist), columns = ['idx','d','maqaf','paseq','break']).set_index('idx')
    return df

#==================================================
# Read and parse
#==================================================
dataframe_list = list()
for book_idx, bookname in enumerate(sorted(os.listdir(source_directory))):
    bookpath = os.path.join(source_directory, bookname)
    book_dataframe_list = list()
    for filename in sorted(os.listdir(bookpath)):
        with open(os.path.join(bookpath, filename)) as f:
            chapterlist = json.load(f)['text']
        book_dataframe_list.append(chapterlist_to_dataframe(chapterlist))
    book_df = book_dataframe_list[0][['d']].rename(columns={'d':'d0'})
    for i, dataframe in enumerate(book_dataframe_list[1:]):
        assert (book_df.index != dataframe.index).sum() == 0
        dataframe = dataframe if i == 1 else dataframe[['d']]
        book_df = book_df.join(dataframe.rename(columns={'d':'d{}'.format(i+1)}), how='left')
    book_df.index = ['{}.{}'.format(book_idx + 1, k) for k in book_df.index]
    dataframe_list.append(book_df)
torah_df = pd.concat(dataframe_list)

#==================================================
# Order and format
#==================================================
torah_df['book'] = [float(k.split('.')[0]) for k in torah_df.index]
torah_df['chapter'] = [float(k.split('.')[1]) for k in torah_df.index]
torah_df['verse'] = [float(k.split('.')[2]) for k in torah_df.index]
torah_df['word'] = [float(k.split('.')[-1]) for k in torah_df.index]
torah_df = torah_df.sort_values(['book','chapter','verse','word']).drop(['book','chapter','verse','word'], axis = 1)
torah_df = torah_df[['d0','d1','d2','maqaf','paseq','break']].reset_index().rename(columns={'index':'idx'})

#==================================================
# Identify nikkud and tropes
#==================================================
def unicode_nikkud_names(s):
    charnamelist = s.encode('ascii','namereplace').decode().split('\\N')[1:]
    nikkudlist = [k.replace('HEBREW POINT','').replace('{','').replace('}','').strip() for k in charnamelist if 'HEBREW POINT' in k]
    return nikkudlist

def unicode_trope_names(s):
    charnamelist = s.encode('ascii','namereplace').decode().split('\\N')[1:]
    tropelist = [k.replace('HEBREW ACCENT','').replace('{','').replace('}','').strip().lower() for k in charnamelist if 'HEBREW ACCENT' in k]
    tropelist = ', '.join([k.replace(' ','-') for k in tropelist])
    return tropelist

torah_df['trope'] = [unicode_trope_names(k) for k in torah_df.d2]

#==================================================
# Export
#==================================================
target_filepath = os.path.join(target_directory, 'words.csv')
torah_df.to_csv(target_filepath, index = False)
