#==================================================
# Imports
#==================================================
import os
import json
import requests
from datetime import datetime

#==================================================
# Function: get Sefaria Tanach
#==================================================
def get_sefaria_tanach():

    # Identify project root and define the target directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    project_root = script_directory.split('/src/d_var')[0]
    target_directory = os.path.join(project_root, 'data/external/sefaria_tanach')

    # Get user input
    if os.path.isdir(target_directory):
        modification_timestamp = os.path.getmtime(target_directory)
        last_modified_datetime = datetime.fromtimestamp(modification_timestamp)
        keyboard_input = input('The target directory {} was last modified on {}. Overwrite (y/n)?'.format(target_directory, str(last_modified_datetime)))

    else:
        keyboard_input = input('Download Sefaria Tanach (y/n)?')


    # Sefaria Tanach source-target dictionary
    source_target_dict = {
        'genesis': {
            'directory': os.path.join(target_directory, '01_genesis')
        },
    }
    source_target_dict['genesis'].update({
        'texts': {
            'text_only': {
                'source': "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/refs/heads/master/json/Tanakh/Torah/Genesis/Hebrew/Tanach%20with%20Text%20Only.json",
                'target': os.path.join(source_target_dict['genesis']['directory'], 'gen01.json'),
            },
            'text_with_nikkud': {
                'source': "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/refs/heads/master/json/Tanakh/Torah/Genesis/Hebrew/Tanach%20with%20Nikkud.json",
                'target': os.path.join(source_target_dict['genesis']['directory'], 'gen02.json'),
            },
            'text_with_taamei_hamikra': {
                'source': "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/refs/heads/master/json/Tanakh/Torah/Genesis/Hebrew/Tanach%20with%20Ta'amei%20Hamikra.json",
                'target': os.path.join(source_target_dict['genesis']['directory'], 'gen03.json'),
            },
        } 
    })

    # Get data and write to file
    if keyboard_input.lower() == 'y':
        for book in source_target_dict.values():
            if not os.path.isdir(book['directory']):
                os.makedirs(book['directory'])
            for text in book['texts'].values():
                response = requests.get(text['source'])
                text_json = response.json()
                with open(text['target'], 'w', encoding = 'utf8') as f:
                    json.dump(text_json, f, ensure_ascii = False)
