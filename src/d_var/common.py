#==================================================
# Imports
#==================================================
import os

#==================================================
# Function: get project root
#==================================================
def get_project_root():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    project_root = script_directory.split('/src/d_var')[0]
    return project_root