#==================================================
# Imports
#==================================================
import os
import d_var as dv

#==================================================
# Function: get Sefaria Tanach
#==================================================
def chapter_to_html(book='genesis', chapter=1):


    # Identify project root and define the target directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    project_root = script_directory.split('/src/d_var')[0]
    target_directory = os.path.join(project_root, 'web')
    
    # Construct the target filepath
    target_filename = '{}{:02d}.html'.format(book, chapter)
    target_filepath = os.path.join(target_directory, target_filename)

    # Load pagebase
    pagebase_filepath = os.path.join(target_directory, 'base', 'pagebase.html')
    with open(pagebase_filepath, 'r') as f:
        pagebase = f.read()

    # Build html
    html_top = pagebase.split('<h2>Genesis 1</h2>')[0] + f'<h2>{book.capitalize()} {chapter}</h2>\n'

    # Center
    html_center = ''

    torah_df = dv.torah()
    
    for verse_idx in range(1,12):
        verse_df = torah_df[(torah_df.book == 1) & (torah_df.chapter==1) & (torah_df.verse==verse_idx)]
        aa = ' '.join(['<span class="word" id="{}">{}</span>'.format(k[0],k[1]) for k in zip(verse_df.idx, verse_df.d2)])

        html_center += '\t\t<div class="clause">\n'
        html_center += f'\t\t\t<p class="label">verse {verse_idx} • clause 1</p>\n'
        # html_center += f'\t\t\t<p class="hebrew">{dv.verse(1, chapter, verse_idx)}</p>\n'
        html_center += f'\t\t\t<p class="hebrew">{aa}</p>\n'
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