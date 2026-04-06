#==================================================
# Imports
#==================================================
import os
import json
import shutil
import requests
from datetime import datetime

import d_var as dv  

#==================================================
# Function: get Sefaria Tanach
#==================================================
def get_sefaria_tanach():

    # Identify project root and define the target directory
    project_root = dv.get_project_root()
    target_directory = os.path.join(project_root, 'data/external/sefaria_tanach')
    temp_directory = os.path.join(project_root, 'data/external', 'temp_{}'.format(''.join(filter(str.isalnum, str(datetime.now())))))

    # Get user input
    if os.path.isdir(target_directory):
        modification_timestamp = os.path.getmtime(target_directory)
        last_modified_datestring = datetime.fromtimestamp(modification_timestamp).strftime('%Y-%m-%dT%H:%M:%S')
        keyboard_input = input('\nThe target directory {} was last modified on {}. Overwrite (y/n)? '.format(target_directory, last_modified_datestring))

    else:
        keyboard_input = input('\nDownload Sefaria Tanach (y/n)? ')


    # Sefaria Tanach source-target dictionary
    repo = 'https://github.com/Sefaria/Sefaria-Export'
    source_target_dict = {
        'genesis': {
            'directory': os.path.join(temp_directory, '01_genesis'),
            'repo': repo,
        },
        'exodus': {
            'directory': os.path.join(temp_directory, '02_exodus'),
            'repo': repo,
        },
        'leviticus': {
            'directory': os.path.join(temp_directory, '03_leviticus'),
            'repo': repo,
        },
        'numbers': {
            'directory': os.path.join(temp_directory, '04_numbers'),
            'repo': repo,
        },
        'deuteronomy': {
            'directory': os.path.join(temp_directory, '05_deuteronomy'),
            'repo': repo,
        },
    }
    source_target_dict['genesis'].update({
        'texts': {
            'text_only': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Genesis/Hebrew/Tanach%20with%20Text%20Only.json",
                'target': os.path.join(source_target_dict['genesis']['directory'], 'genesis.json'),
            },
            'text_with_nikkud': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Genesis/Hebrew/Tanach%20with%20Nikkud.json",
                'target': os.path.join(source_target_dict['genesis']['directory'], 'genesis_with_nikkud.json'),
            },
            'text_with_taamei_hamikra': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Genesis/Hebrew/Tanach%20with%20Ta'amei%20Hamikra.json",
                'target': os.path.join(source_target_dict['genesis']['directory'], 'genesis_with_taamei_hamikra.json'),
            },
        } 
    })
    source_target_dict['exodus'].update({
        'texts': {
            'text_only': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Exodus/Hebrew/Tanach%20with%20Text%20Only.json",
                'target': os.path.join(source_target_dict['exodus']['directory'], 'exodus.json'),
            },
            'text_with_nikkud': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Exodus/Hebrew/Tanach%20with%20Nikkud.json",
                'target': os.path.join(source_target_dict['exodus']['directory'], 'exodus_with_nikkud.json'),
            },
            'text_with_taamei_hamikra': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Exodus/Hebrew/Tanach%20with%20Ta'amei%20Hamikra.json",
                'target': os.path.join(source_target_dict['exodus']['directory'], 'exodus_with_taamei_hamikra.json'),
            },
        } 
    })
    source_target_dict['leviticus'].update({
        'texts': {
            'text_only': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Leviticus/Hebrew/Tanach%20with%20Text%20Only.json",
                'target': os.path.join(source_target_dict['leviticus']['directory'], 'leviticus.json'),
            },
            'text_with_nikkud': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Leviticus/Hebrew/Tanach%20with%20Nikkud.json",
                'target': os.path.join(source_target_dict['leviticus']['directory'], 'leviticus_with_nikkud.json'),
            },
            'text_with_taamei_hamikra': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Leviticus/Hebrew/Tanach%20with%20Ta'amei%20Hamikra.json",
                'target': os.path.join(source_target_dict['leviticus']['directory'], 'leviticus_with_taamei_hamikra.json'),
            },
        } 
    })
    source_target_dict['numbers'].update({
        'texts': {
            'text_only': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Numbers/Hebrew/Tanach%20with%20Text%20Only.json",
                'target': os.path.join(source_target_dict['numbers']['directory'], 'numbers.json'),
            },
            'text_with_nikkud': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Numbers/Hebrew/Tanach%20with%20Nikkud.json",
                'target': os.path.join(source_target_dict['numbers']['directory'], 'numbers_with_nikkud.json'),
            },
            'text_with_taamei_hamikra': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Numbers/Hebrew/Tanach%20with%20Ta'amei%20Hamikra.json",
                'target': os.path.join(source_target_dict['numbers']['directory'], 'numbers_with_taamei_hamikra.json'),
            },
        } 
    })
    source_target_dict['deuteronomy'].update({
        'texts': {
            'text_only': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Deuteronomy/Hebrew/Tanach%20with%20Text%20Only.json",
                'target': os.path.join(source_target_dict['deuteronomy']['directory'], 'deuteronomy.json'),
            },
            'text_with_nikkud': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Deuteronomy/Hebrew/Tanach%20with%20Nikkud.json",
                'target': os.path.join(source_target_dict['deuteronomy']['directory'], 'deuteronomy_with_nikkud.json'),
            },
            'text_with_taamei_hamikra': {
                'source': "https://storage.googleapis.com/sefaria-export/json/Tanakh/Torah/Deuteronomy/Hebrew/Tanach%20with%20Ta'amei%20Hamikra.json",
                'target': os.path.join(source_target_dict['deuteronomy']['directory'], 'deuteronomy_with_taamei_hamikra.json'),
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
                    text['license'] = text_json.get('license')
                    with open(text['target'], 'w', encoding = 'utf8') as f:
                        json.dump(text_json, f, ensure_ascii = False)

            if os.path.isdir(target_directory):
                shutil.rmtree(target_directory)
            shutil.move(temp_directory, target_directory)
            print('Success. Files have been written to {}'.format(target_directory))

        except Exception as e:
            print('Failed to download source texts: {}'.format(e))

    return source_target_dict


#============================================================
# Function: get Strong's Hebrew Dictionary and WLC mapping
#============================================================
def get_openscriptures_strongs():

    # Identify project root and define the target directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    project_root = script_directory.split('/src/d_var')[0]
    target_directory = os.path.join(project_root, 'data/external/openscriptures_strongs')
    temp_directory = os.path.join(project_root, 'data/external', 'temp_{}'.format(''.join(filter(str.isalnum, str(datetime.now())))))

    # Get user input
    if os.path.isdir(target_directory):
        modification_timestamp = os.path.getmtime(target_directory)
        last_modified_datestring = datetime.fromtimestamp(modification_timestamp).strftime('%Y-%m-%dT%H:%M:%S')
        keyboard_input = input('\nThe target directory {} was last modified on {}. Overwrite (y/n)? '.format(target_directory, last_modified_datestring))

    else:
        keyboard_input = input("\nDownload Strong's Hebrew Dictionary and WLC mapping from OpenScriptures (y/n)? ")


    # OpenScriptures Strong's source-target dictionary
    source_target_dict = {
        'strongs_hebrew_dictionary': {
            'source': 'https://raw.githubusercontent.com/openscriptures/strongs/refs/heads/master/hebrew/strongs-hebrew-dictionary.js',
            'target': os.path.join(temp_directory, 'strongs_hebrew_dictionary.js'),
            'repo': 'https://github.com/openscriptures/strongs',
            'license': 'No license specified in repository',
        },
        'wlc_mapping': {
            'source': 'https://raw.githubusercontent.com/openscriptures/morphhb/refs/heads/master/oxlos-import/wlc_cons.txt',
            'target': os.path.join(temp_directory, 'wlc_cons.txt'),
            'repo': 'https://github.com/openscriptures/morphhb',
            'license': 'WLC text is Public Domain. Lemma and morphology data are CC-BY 4.0',
        },
    }


    # Get data and write to file
    if keyboard_input.lower() == 'y':
        try:
            os.makedirs(temp_directory)
            for text in source_target_dict.values():
                response = requests.get(text['source'])
                textstring = response.text
                with open(text['target'], 'w', encoding = 'utf8') as f:
                    f.write(textstring)

            if os.path.isdir(target_directory):
                shutil.rmtree(target_directory)
            shutil.move(temp_directory, target_directory)
            print('Success. Files have been written to {}'.format(target_directory))

        except Exception as e:
            print('Failed to download source texts: {}'.format(e))

    return source_target_dict


#==================================================
# Function: write manifest
#==================================================
def write_manifest(target_directory, sefaria_dict, openscriptures_dict):
    manifest_filepath = os.path.join(target_directory, 'SOURCES.md')
    datestring = datetime.now().strftime('%Y-%m-%d')

    table_header = ['| File | License | Download Date |', '| --- | --- | --- |']

    lines = [
        '# External Data Sources',
        '',
        '## [Sefaria-Export](https://github.com/Sefaria/Sefaria-Export)',
        '',
    ] + table_header

    for book in sefaria_dict.values():
        for text in book.get('texts', {}).values():
            filename = os.path.basename(text['target'])
            license = text.get('license', 'unknown')
            lines.append('| [{}]({}) | {} | {} |'.format(
                filename, text['source'], license, datestring))

    lines += ['', '## [OpenScriptures](https://github.com/openscriptures)', ''] + table_header

    for entry in openscriptures_dict.values():
        filename = os.path.basename(entry['target'])
        license = entry.get('license', 'unknown')
        lines.append('| [{}]({}) | {} | {} |'.format(
            filename, entry['source'], license, datestring))

    lines.append('')

    with open(manifest_filepath, 'w') as f:
        f.write('\n'.join(lines))


#==================================================
# Function: get external files
#==================================================
def get_external_files():
    sefaria_dict = get_sefaria_tanach()
    openscriptures_dict = get_openscriptures_strongs()

    project_root = dv.get_project_root()
    target_directory = os.path.join(project_root, 'data/external')
    write_manifest(target_directory, sefaria_dict, openscriptures_dict)