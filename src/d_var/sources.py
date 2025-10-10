#==================================================
# Imports
#==================================================
import os
import json
import shutil
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
    temp_directory = os.path.join(project_root, 'data/external', 'temp_{}'.format(''.join(filter(str.isalnum, str(datetime.now())))))

    # Get user input
    if os.path.isdir(target_directory):
        modification_timestamp = os.path.getmtime(target_directory)
        last_modified_datestring = datetime.fromtimestamp(modification_timestamp).strftime('%Y-%m-%dT%H:%M:%S')
        keyboard_input = input('The target directory {} was last modified on {}. Overwrite (y/n)? '.format(target_directory, last_modified_datestring))

    else:
        keyboard_input = input('Download Sefaria Tanach (y/n)? ')


    # Sefaria Tanach source-target dictionary
    source_target_dict = {
        'genesis': {
            'directory': os.path.join(temp_directory, '01_genesis')
        },
        'exodus': {
            'directory': os.path.join(temp_directory, '02_exodus')
        },
    }
    source_target_dict['genesis'].update({
        'texts': {
            'text_only': {
                'source': "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/refs/heads/master/json/Tanakh/Torah/Genesis/Hebrew/Tanach%20with%20Text%20Only.json",
                'target': os.path.join(source_target_dict['genesis']['directory'], 'genesis.json'),
            },
            'text_with_nikkud': {
                'source': "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/refs/heads/master/json/Tanakh/Torah/Genesis/Hebrew/Tanach%20with%20Nikkud.json",
                'target': os.path.join(source_target_dict['genesis']['directory'], 'genesis_with_nikkud.json'),
            },
            'text_with_taamei_hamikra': {
                'source': "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/refs/heads/master/json/Tanakh/Torah/Genesis/Hebrew/Tanach%20with%20Ta'amei%20Hamikra.json",
                'target': os.path.join(source_target_dict['genesis']['directory'], 'genesis_with_taamei_hamikra.json'),
            },
        } 
    })
    source_target_dict['exodus'].update({
        'texts': {
            'text_only': {
                'source': "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/refs/heads/master/json/Tanakh/Torah/Exodus/Hebrew/Tanach%20with%20Text%20Only.json",
                'target': os.path.join(source_target_dict['exodus']['directory'], 'exodus.json'),
            },
            'text_with_nikkud': {
                'source': "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/refs/heads/master/json/Tanakh/Torah/Exodus/Hebrew/Tanach%20with%20Nikkud.json",
                'target': os.path.join(source_target_dict['exodus']['directory'], 'exodus_with_nikkud.json'),
            },
            'text_with_taamei_hamikra': {
                'source': "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/refs/heads/master/json/Tanakh/Torah/Exodus/Hebrew/Tanach%20with%20Ta'amei%20Hamikra.json",
                'target': os.path.join(source_target_dict['exodus']['directory'], 'exodus_with_taamei_hamikra.json'),
            },
        } 
    })

    # Get data and write to file
    if keyboard_input.lower() == 'y':
        try:
            for book in source_target_dict.values():
                if not os.path.isdir(book['directory']):
                    os.makedirs(book['directory'])
                for text in book['texts'].values():
                    response = requests.get(text['source'])
                    text_json = response.json()
                    with open(text['target'], 'w', encoding = 'utf8') as f:
                        json.dump(text_json, f, ensure_ascii = False)

            if os.path.isdir(target_directory):
                shutil.rmtree(target_directory)
            shutil.move(temp_directory, target_directory)
            print('Success. Files have been written to {}'.format(target_directory))

        except:
            print('Failed to download source texts.')
