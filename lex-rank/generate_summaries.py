from sumy_summary import getSumySummary
from summary import getLexRankSummary

opfile = "output.txt"
output_file = open(opfile, 'w')

return_count = "10%"
fpath = "para2.txt"

sumy_summary = getSumySummary(fpath,return_count)

lex_rank_summary = getLexRankSummary(fpath,return_count)

output_file.write('Filename=' + fpath + '\n')
output_file.write('Reference Summary' + '\n')
output_file.write(sumy_summary + '\n')
output_file.write('Our Summary' + '\n')
output_file.write(lex_rank_summary)
output_file.close()

