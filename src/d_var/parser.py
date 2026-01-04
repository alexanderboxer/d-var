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
data_directory = os.path.join(project_root,'data','external','sefaria_tanach') # Sefaria


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



def torah():
    #==================================================
    # Read and parse
    #==================================================
    dataframe_list = list()
    for book_idx, bookname in enumerate(sorted(os.listdir(data_directory))):
        bookpath = os.path.join(data_directory, bookname)
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
    # Word counts
    #==================================================
    #torah_df['n'] = torah_df.groupby('strongs_number').cumcount() + 1
    #torah_df['N'] = torah_df.groupby('strongs_number')['strongs_number'].transform('count')
    #torah_df['strongs_count'] = [(int(k[0]), int(k[1])) if not pd.isna(k[2]) else None for k in zip(torah_df.n, torah_df.N, torah_df.strongs_number)]

    torah_df['n0'] = torah_df.groupby('d0').cumcount() + 1
    torah_df['N0'] = torah_df.groupby('d0')['d0'].transform('count')
    torah_df['d0_count'] = [(int(k[0]), int(k[1])) if not pd.isna(k[2]) else None for k in zip(torah_df.n0, torah_df.N0, torah_df.d0)]

    torah_df['n1'] = torah_df.groupby('d1').cumcount() + 1
    torah_df['N1'] = torah_df.groupby('d1')['d1'].transform('count')
    torah_df['d1_count'] = [(int(k[0]), int(k[1])) if not pd.isna(k[2]) else None for k in zip(torah_df.n1, torah_df.N1, torah_df.d1)]

    torah_df['n2'] = torah_df.groupby('d2').cumcount() + 1
    torah_df['N2'] = torah_df.groupby('d2')['d2'].transform('count')
    torah_df['d2_count'] = [(int(k[0]), int(k[1])) if not pd.isna(k[2]) else None for k in zip(torah_df.n2, torah_df.N2, torah_df.d2)]

    torah_df = torah_df.drop(['n0','N0','n1','N1','n2','N2'], axis=1)

    return torah_df 



def verse(book_idx, chapter_idx, verse_idx, level=3):
    bookdirs = sorted(os.listdir(data_directory))
    bookdir = bookdirs[book_idx-1]
    bookpath = os.path.join(data_directory, bookdir)
    filenames = sorted(os.listdir(bookpath))
    filename = filenames[level-1]
    filepath = os.path.join(bookpath, filename)
    with open(filepath) as f:
        chapterlist = json.load(f)['text']
    chapter_text = chapterlist[chapter_idx-1]
    verse_text = chapter_text[verse_idx-1]

    return verse_text