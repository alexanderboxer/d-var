#==================================================
# Imports
#==================================================
import os
import re
import json
import d_var as dv

#==================================================
# Function: create html file for a given chapter
#==================================================
def chapter_to_html(book='genesis', chapter=1):

    # Paths
    project_root = dv.get_project_root()
    pagebase_filepath = os.path.join(project_root,'data','templates','pagebase.html')
    bookname2directory_dict = {'genesis':'01_genesis','exodus':'02_exodus','leviticus':'03_leviticus','numbers':'04_numbers','deuteronomy':'05_deuteronomy'}
    html_target_directory = os.path.join(project_root,'web','{}'.format(bookname2directory_dict.get(book)))
    html_target_filename = '{}{:02d}.html'.format(book, chapter)
    html_target_filepath = os.path.join(html_target_directory, html_target_filename)
    js_target_directory = os.path.join(project_root,'web','js')
    js_target_filename = re.sub('.html','.js',html_target_filename)
    js_target_filepath = os.path.join(js_target_directory, js_target_filename)

    # Load pagebase
    pagebase_filepath = os.path.join(pagebase_filepath)
    with open(pagebase_filepath, 'r') as f:
        pagebase = f.read()

    # Load dataframe
    torah_df = dv.torah()
    chapter_df = torah_df[(torah_df.book == 1) & (torah_df.chapter == 1)].copy()
    
    # Export javascript
    wordstats_dict = chapter_df.set_index('idx').to_dict(orient='index')
    json_string = json.dumps(wordstats_dict, ensure_ascii=False)
    js = '''const j2 = JSON.parse('{}');'''.format(json_string)
    with open(js_target_filepath, 'w') as f:
        f.write(js)


    # Build html
    html_top = pagebase.split('</header>')[0] + '</header>\n'
    html_top = re.sub('<link rel="stylesheet" href=".*?">', '<link rel="stylesheet" href="../css/style.css">', html_top)
    html_top = re.sub(r'  ', '\t', html_top)

    # Center
    html_center = '\t<div id="main">\n\t\t<article>\n'


    
    
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
    html_foot = re.sub('<script src=".*?">', '<script src="../js/{}">'.format(js_target_filename), html_foot, count=1)
    html_foot = re.sub('<script src=".*?dvar.js">', '<script src="../js/dvar.js">', html_foot)
    html_foot = re.sub(r'  ', '\t', html_foot)

    # Export
    s = html_top + html_center + html_side + html_foot
    s = re.sub('\t', '  ', s)

    with open(html_target_filepath,'w') as f:
        f.write(s)