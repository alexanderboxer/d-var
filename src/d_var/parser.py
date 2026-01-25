'''
parse sourcetexts
'''
#==================================================
# Imports
#==================================================
import os 
import json
import pandas as pd

import d_var as dv


#==================================================
# Paths
#==================================================
project_root = dv.get_project_root()
sefaria_tanach_directory = os.path.join(project_root,'data','external','sefaria_tanach') # Sefaria
strongs_directory = os.path.join(project_root,'data','external','openscriptures_strongs') # Strongs

# Auxiliary 
clausebreaks_filepath = os.path.join(project_root,'data','hand_parsed','auxiliary','clausebreaks.json') # clause breaks
strongs2root_filepath = os.path.join(project_root,'data','hand_parsed','auxiliary','strongs2root.json') # clause breaks

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
# Function: letters only
#==================================================
def letters_only(s):
    try:
        charzip = list(zip(s.encode('ascii','namereplace').decode().split('\\N')[1:], [ord(k) for k in s.encode('unicode-escape').decode('unicode-escape')]))
        return ''.join([chr(k[1]) for k in charzip if 'HEBREW LETTER' in k[0]])
    except:
        return None


#==================================================
# Function: create Torah dataframe
#==================================================
def torah():

    #==================================================
    # Read and parse
    #==================================================
    dataframe_list = list()
    for book_idx, bookname in enumerate(sorted(os.listdir(sefaria_tanach_directory))):
        bookpath = os.path.join(sefaria_tanach_directory, bookname)
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
    torah_df['book'] = [int(k.split('.')[0]) for k in torah_df.index]
    torah_df['chapter'] = [int(k.split('.')[1]) for k in torah_df.index]
    torah_df['verse'] = [int(k.split('.')[2]) for k in torah_df.index]
    torah_df['word'] = [int(k.split('.')[-1]) for k in torah_df.index]
    torah_df = torah_df.sort_values(['book','chapter','verse','word'])
    torah_df = torah_df[['book','chapter','verse','word','d0','d1','d2','maqaf','paseq','break']].reset_index().rename(columns={'index':'idx'})

    #==================================================
    # Identify nikkud and tropes
    #==================================================
    def unicode_nikkud_names(s):
        charnamelist = s.encode('ascii','namereplace').decode().split('\\N')[1:]
        nikkudlist = [k.replace('HEBREW POINT','').replace('{','').replace('}','').strip() for k in charnamelist if 'HEBREW POINT' in k]
        return nikkudlist

    def unicode_trope_names(s):
        charnamelist = s.encode('ascii','namereplace').decode().split('\\N')[1:]
        tropelist = [k.replace('HEBREW ACCENT','').replace('HEBREW PUNCTUATION','').replace('{','').replace('}','').strip().lower() for k in charnamelist if ('HEBREW ACCENT' in k) or ('SOF PASUQ' in k)]
        tropelist = ', '.join([k.replace(' ','-') for k in tropelist])
        return tropelist

    torah_df['trope'] = [unicode_trope_names(k) for k in torah_df.d2]

    #==================================================
    # Remove sof-pasuq from d1 forms
    #==================================================
    torah_df['d1'] = [k.replace('׃','') for k in torah_df.d1]

    #==================================================
    # Parse Strong numbers and merge
    #==================================================
    stronglist_filename = 'wlc_cons.txt'
    stronglist_filepath = os.path.join(strongs_directory, stronglist_filename)
    strongs_df = pd.read_csv(stronglist_filepath, sep=r'\s+', dtype={0:str, 1:str, 2:str, 3:str}, names= ['book','idx','strongs_number','d0'])
    strongs_df['d0'] = [k.replace('/','') for k in strongs_df.d0]
    bookname_dict = {
        'Gen': 1,
        'Exod': 2,
        'Lev': 3,
        'Nu': 4,
        'Deut': 5,
    }
    strongs_df['book'] = [bookname_dict[k] if k in bookname_dict.keys() else k for k in strongs_df.book]
    strongs_df['idx'] = ['{}.{}'.format(k[0], k[1].replace(':','.')) for k in zip(strongs_df.book, strongs_df.idx)]
    strongs_df = strongs_df.drop('book', axis=1)

    # merge
    torah_df = torah_df.merge(strongs_df, how='left', on=['idx','d0'])
    torah_df['strongs_number'] = [str(int(k)) if (pd.notna(k)) and (int(k)>0) else None for k in torah_df.strongs_number]

    #==================================================
    # Append Strongs lemmas
    #==================================================
    strongs_dictionary_filename = 'strongs_hebrew_dictionary.js'
    strongs_dictionary_filepath = os.path.join(strongs_directory, strongs_dictionary_filename)
    with open(strongs_dictionary_filepath, 'r') as f:
        strongstxt = f.read()
    strongs_json = strongstxt.replace('\n','').split('var strongsHebrewDictionary = ')[-1].split(';module.exports')[0]
    strongs_dictionary = json.loads(strongs_json)

    # append
    torah_df['strongs_lemma'] = [strongs_dictionary.get('H{}'.format(k),{}).get('lemma') for k in torah_df.strongs_number]

    # plain lemma
    torah_df['lemma'] = [letters_only(k) for k in torah_df.strongs_lemma]
    torah_df = torah_df.drop('strongs_lemma', axis=1)

    #==================================================
    # Append Roots
    #==================================================
    try:
        with open(strongs2root_filepath, 'r') as f:
            strongs2root_dict = json.load(f)
    except:
        strongs2root_dict = dict()

    torah_df['root'] = [strongs2root_dict.get(str(k),{}).get('root') for k in torah_df.strongs_number]

    #==================================================
    # Word counts
    #==================================================
    n = torah_df.groupby('strongs_number').cumcount() + 1
    N = torah_df.groupby('strongs_number')['strongs_number'].transform('count')
    torah_df['strongs_count'] = [(int(k[0]), int(k[1])) if not pd.isna(k[2]) else (None, None) for k in zip(n, N, torah_df.strongs_number)]

    n0 = torah_df.groupby('d0').cumcount() + 1
    N0 = torah_df.groupby('d0')['d0'].transform('count')
    torah_df['d0_count'] = [(int(k[0]), int(k[1])) if not pd.isna(k[2]) else (None, None) for k in zip(n0, N0, torah_df.d0)]

    n1 = torah_df.groupby('d1').cumcount() + 1
    N1 = torah_df.groupby('d1')['d1'].transform('count')
    torah_df['d1_count'] = [(int(k[0]), int(k[1])) if not pd.isna(k[2]) else (None, None) for k in zip(n1, N1, torah_df.d1)]

    n2 = torah_df.groupby('d2').cumcount() + 1
    N2 = torah_df.groupby('d2')['d2'].transform('count')
    torah_df['d2_count'] = [(int(k[0]), int(k[1])) if not pd.isna(k[2]) else (None, None) for k in zip(n2, N2, torah_df.d2)]

    n3 = torah_df.groupby('root').cumcount() + 1
    N3 = torah_df.groupby('root')['root'].transform('count')
    torah_df['root_count'] = [(int(k[0]), int(k[1])) if not pd.isna(k[2]) else (None, None) for k in zip(n3, N3, torah_df['root'])]

    #==================================================
    # Append hand-parsed clause divisions
    #==================================================
    try:
        with open(clausebreaks_filepath, 'r') as f:
            clausebreak_dict = json.load(f)
    except:
        clausebreak_dict = dict()

    def assign_clause_number(torah_word_index, clausebreak_dict):
        clause_key = '.'.join(torah_word_index.split('.')[:-1])
        word_num = int(torah_word_index.split('.')[-1])
        clausebreak_list = clausebreak_dict.get(clause_key,[1])
        clause_num = len([k for k in clausebreak_list if word_num >= k])
        return max([1, clause_num])

    torah_df['clause'] = [assign_clause_number(k, clausebreak_dict) for k in torah_df.idx]
    head_columns = ['idx','book','chapter','verse','word','clause']
    torah_df = torah_df[head_columns + [k for k in torah_df.columns if k not in head_columns]]

    #==================================================
    # Return
    #==================================================
    return torah_df 



def verse(book_idx, chapter_idx, verse_idx, level=3):
    bookdirs = sorted(os.listdir(sefaria_tanach_directory))
    bookdir = bookdirs[book_idx-1]
    bookpath = os.path.join(sefaria_tanach_directory, bookdir)
    filenames = sorted(os.listdir(bookpath))
    filename = filenames[level-1]
    filepath = os.path.join(bookpath, filename)
    with open(filepath) as f:
        chapterlist = json.load(f)['text']
    chapter_text = chapterlist[chapter_idx-1]
    verse_text = chapter_text[verse_idx-1]

    return verse_text