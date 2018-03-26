import csv
from pandas import DataFrame
import pandas as pd
with open('/Users/lmk/OneDrive - The University of Hong Kong/cloud_computing/Project/behavior_log.csv') as f:
    f_csv = csv.reader(f)
    # headers = next(f_csv)
    i = 1
    d = {}
    for row in f_csv:
        # print (row)
        # d[row[0]+row[1]] = (row[2],row[3],row[4])
        d[(row[0],row[1])] = (row[2], row[3], row[4])
        i+=1
        if i >2000000:
            break

df = DataFrame(data=d)
df.to_csv('/Users/lmk/OneDrive - The University of Hong Kong/cloud_computing/Project/clean_data.csv')

# with open('/Users/lmk/OneDrive - The University of Hong Kong/cloud_computing/Project/cleantest_1.csv',
#           'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile)
#     for k in df.keys():
#         print(df[k])
#
#
#     spamwriter.writerow([k,df[k]])
        #
        # spamwriter.writerow([k,df[k]])
    # spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

# with open('/Users/lmk/OneDrive - The University of Hong Kong/cloud_computing/Project/test.csv', 'w') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=' ',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
#     spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])


