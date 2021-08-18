import ast
import pandas as pd

with open('angeles.txt') as f:
    lines = f.readlines()
    

angles_list = []

for line in lines:
    if line.rstrip():
        angles_list.append(ast.literal_eval(line))
        
        
angles_data = [[angles_list[i][key][1][1] for key in angles_list[0].keys()] for i in range(len(angles_list))]
df = pd.DataFrame(angles_data, columns=list(angles_list[0].keys()))
df.head()


print('Median values:')
print(df.median())
print('')
print('--------------------')
print('Average values:')
print(df.mean())
print('--------------------')
print('Max values:')
print(df.max())
print('--------------------')
print('Min values:')
print(df.min())
