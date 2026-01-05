#==================================================
# Imports
#==================================================
import os
import d_var as dv

#==================================================
# Function: create html file for a given chapter
#==================================================
def chapter_to_html(book='genesis', chapter=1):


    # Paths
    project_root = dv.get_project_root()
    target_directory = os.path.join(project_root, 'web')
    
    # Construct the target filepath
    target_filename = '{}{:02d}.html'.format(book, chapter)
    target_filepath = os.path.join(target_directory, target_filename)

    # Load pagebase
    pagebase_filepath = os.path.join(target_directory, 'base', 'pagebase.html')
    with open(pagebase_filepath, 'r') as f:
        pagebase = f.read()

    # Build html
    html_top = pagebase.split('<div class="main">')[0] + '<div class="main">\n'

    # Center
    html_center = ''

    torah_df = dv.torah()
    
    for verse_idx in range(1,12):
        verse_df = torah_df[(torah_df.book == 1) & (torah_df.chapter==1) & (torah_df.verse==verse_idx)]
        for clause_idx in range(1, 1 + len(set(verse_df.clause))):
            clause_df = verse_df[verse_df.clause==clause_idx]
            separator_list = ['&#x5BE;' if (k is not None) and (k[0] < k[1]) else ' ' for k in clause_df.maqaf]
            aa = ''.join(['<span class="word" id="{}">{}</span>{}'.format(k[0],k[1],k[2]) for k in zip(clause_df.idx, clause_df.d2, separator_list)])

            html_center += '\t\t<div class="clause">\n'
            html_center += f'\t\t\t<p class="label">verse {verse_idx} • clause {clause_idx}</p>\n'
            html_center += '\t\t\t<div class="row">\n'

            html_center += '\t\t\t\t<div class="english">\n'
            html_center += f'\t\t\t\t\t<p>In the beginning</p>\n'
            html_center += '\t\t\t\t</div>\n'

            html_center += '\t\t\t\t<div class="hebrew">\n'
            html_center += f'\t\t\t\t\t<p>{aa}</p>\n'
            html_center += '\t\t\t\t</div>\n'



            html_center += '\t\t\t</div>\n'
            html_center += '\t\t</div>\n'

    html_center += '\t</div><!-- main -->\n'


    # Side
    html_side = '\t<div class="side">' + pagebase.split('<div class="side">')[-1].split('<div class="footer">')[0]

    # Foot
    html_foot = '<div class="footer">' + pagebase.split('<div class="footer">')[-1]

    # Export
    s = html_top + html_center + html_side + html_foot

    with open(target_filepath,'w') as f:
        f.write(s)