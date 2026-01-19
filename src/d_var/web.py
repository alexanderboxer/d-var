#==================================================
# Imports
#==================================================
import os
import re
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
    #pagebase_filepath = os.path.join(target_directory, 'base', 'pagebase.html')
    pagebase_filepath = os.path.join(target_directory, 'pagebase.html')
    with open(pagebase_filepath, 'r') as f:
        pagebase = f.read()

    # Build html
    html_top = pagebase.split('</header>')[0] + '</header>\n'
    html_top = re.sub(r'  ', '\t', html_top)

    # Center
    html_center = '\t<div id="main">\n\t\t<article>\n'


    torah_df = dv.torah()
    
    for verse_idx in range(1,12):
        verse_df = torah_df[(torah_df.book == 1) & (torah_df.chapter==1) & (torah_df.verse==verse_idx)]
        for clause_idx in range(1, 1 + len(set(verse_df.clause))):
            clause_df = verse_df[verse_df.clause==clause_idx]
            separator_list = ['&#x5BE;' if (k is not None) and (k[0] < k[1]) else ' ' for k in clause_df.maqaf]
            aa = ''.join(['<span class="word" id="{}">{}</span>{}'.format(k[0],k[1],k[2]) for k in zip(clause_df.idx, clause_df.d2, separator_list)])

            # open divs
            html_center += '\t\t\t<div class="clause">\n'
            html_center += f'\t\t\t\t<p class="label">verse {verse_idx} • clause {clause_idx}</p>\n'
            html_center += '\t\t\t\t<div class="row">\n'

            # English 
            html_center += '\t\t\t\t\t<div class="english">\n'
            html_center += f'\t\t\t\t\t\t<p>In the beginning</p>\n'
            html_center += '\t\t\t\t\t</div>\n'

            # Hebrew
            html_center += '\t\t\t\t\t<div class="hebrew">\n'
            html_center += f'\t\t\t\t\t\t<p>{aa}</p>\n'
            html_center += '\t\t\t\t\t</div>\n'
            
            # close divs
            html_center += '\t\t\t\t</div><!-- row -->\n'
            html_center += '\t\t\t</div><!-- clause -->\n'

    html_center += '\t\t</article>\n'

    # Side
    html_side = '\t\t<aside>\n' + pagebase.split('<aside>')[-1].split('</aside>')[0].replace('  ','\t') + '</aside>\n\t</div><!-- main -->\n'


    # Foot
    html_foot = '\t<footer>' + pagebase.split('<footer>')[-1]
    html_foot = re.sub(r'  ', '\t', html_foot)

    # Export
    s = html_top + html_center + html_side + html_foot
    s = re.sub('\t', '  ', s)

    with open(target_filepath,'w') as f:
        f.write(s)