#==================================================
# Imports
#==================================================
import requests

#==================================================
# Function: state initialization
#==================================================
def get_sefaria_tanach():
    genesis_with_text_only_json_url = 'https://raw.githubusercontent.com/Sefaria/Sefaria-Export/refs/heads/master/json/Tanakh/Torah/Genesis/Hebrew/Tanach%20with%20Text%20Only.json'
    response = requests.get(genesis_with_text_only_json_url)
    gg = response.json()

    return gg

