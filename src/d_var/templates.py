#==================================================
# Imports
#==================================================
import os
import json

#==================================================
# Function: get Sefaria Tanach
#==================================================
def create_clausebreaks_template_file():

    # Identify project root and define the target filepath
    script_directory = os.path.dirname(os.path.abspath(__file__))
    project_root = script_directory.split('/src/d_var')[0]
    data_directory = os.path.join(project_root,'data','external','sefaria_tanach') # Sefaria
    target_directory = os.path.join(project_root, 'data','templates')
    target_filename = 'template_clausebreaks.json'
    target_filepath = os.path.join(target_directory, target_filename)

    # Create a clausebreak template file with a default list ([0]) for each verse
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
                clausebreak_dict.update({key: [0]})

    # Export
    with open(target_filepath, 'w') as f:
        json.dump(clausebreak_dict, f, sort_keys=True)