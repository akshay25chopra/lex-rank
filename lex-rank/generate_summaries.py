from sumy_summary import getSumySummary
from summary import getLexRankSummary
import os

opfile = "output.txt"
output_file = open(opfile, 'w')

return_count = "10%"

# path= r"data/para2.txt"
path = r"/Users/arorai/Downloads/Timeline17/Data/bpoil_guardian/InputDocs"
# path = "/home/shivalik/Downloads/Timeline17/Data/bpoil_foxnews/InputDocs"

for folders, subs, files in os.walk(path):
    for name in files:
        if '.DS_Store' in name:
            continue
        filePath = os.path.join(folders, name)
        # print(filePath)
        sumy_summary = getSumySummary(filePath, return_count)
        lex_rank_summary = getLexRankSummary(filePath, return_count)

        output_file.write('Filename=' + name + '\n')
        output_file.write('Reference Summary' + '\n')
        output_file.write(sumy_summary + '\n')
        output_file.write('Our Summary' + '\n')
        output_file.write(lex_rank_summary + '\n\n')

output_file.close()

