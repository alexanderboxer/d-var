#==================================================
# Imports
#==================================================
import os
import json

import d_var as dv


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
# Function: create lemma-root template json
#==================================================
def create_strongs2root_template():

    # Paths
    project_root = dv.get_project_root()
    source_filepath = os.path.join(project_root,'data','external','openscriptures_strongs','strongs_hebrew_dictionary.js') 
    target_directory = os.path.join(project_root, 'data','templates')
    target_filename = 'template_strongs2root.json'
    target_filepath = os.path.join(target_directory, target_filename)

    # Load data
    with open(source_filepath, 'r') as f:
        strongstxt = f.read()
    strongs_json = strongstxt.replace('\n','').split('var strongsHebrewDictionary = ')[-1].split(';module.exports')[0]
    strongs_dictionary = json.loads(strongs_json)

    # strongs_to_root
    strongs_lemma_tuplelist = [(k, strongs_dictionary[k].get('lemma')) for k in strongs_dictionary.keys()]
    strongs2root_dict = dict([(int(k[0].replace('H','')), {'lemma': k[1], 'root': None}) for k in strongs_lemma_tuplelist])

    # Export
    with open(target_filepath, 'w') as f:
        json.dump(strongs2root_dict, f, sort_keys=False, ensure_ascii=False)


#==================================================
# Function: create clausebreaks template file
#==================================================
def create_clausebreaks_template():

    # Paths
    project_root = dv.get_project_root()
    data_directory = os.path.join(project_root,'data','external','sefaria_tanach') # Sefaria
    target_directory = os.path.join(project_root, 'data','templates')
    target_filename = 'template_clausebreaks.json'
    target_filepath = os.path.join(target_directory, target_filename)

    # Create a clausebreak template file with a default list ([1]) for each verse
    clausebreak_dict = dict()
    for book_idx, bookname in enumerate(sorted(os.listdir(data_directory))):
        bookpath = os.path.join(data_directory, bookname)
        sourcetext_filename = sorted(os.listdir(bookpath))[-1] # any file will serve; by default take the last (text with taamei hamikra)
        sourcetext_filepath = os.path.join(bookpath, sourcetext_filename)
        with open(sourcetext_filepath) as f:
            chapterlist = json.load(f)['text']
        for chapter_idx, chapter in enumerate(chapterlist):
            for verse_idx, verse in enumerate(chapter):
                key = '{}.{}.{}'.format(book_idx + 1, chapter_idx + 1, verse_idx + 1)
                clausebreak_dict.update({key: [1]})

    # Export
    with open(target_filepath, 'w') as f:
        json.dump(clausebreak_dict, f, sort_keys=False)


#==================================================
# Function: create template files
#==================================================
def create_template_datafiles():

    # 1. 
    create_strongs2root_template()

    # 2. 
    create_clausebreaks_template()