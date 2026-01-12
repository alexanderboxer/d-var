# ==================================================
# Imports
# ==================================================
import json

import d_var as dv

# ==================================================
# 
# ==================================================

#dv.get_external_files()

# dv.create_clausebreaks_template_file()

# tdf = dv.torah()


# wordstat_dict = tdf[(tdf.book==1) & (tdf.chapter==1)].set_index('idx').to_dict(orient='index')
# target_filepath = 'web/wordstats.js'
# json_string = json.dumps(wordstat_dict)
# s = '''const j2 = JSON.parse('{}');'''.format(json_string)
# with open(target_filepath, 'w') as f:
#     f.write(s)

# target_filepath2 = 'web/wordstats.json'loop
# with open(target_filepath2, 'w') as f:
#     json.dump(wordstat_dict, f)


dv.chapter_to_html()
