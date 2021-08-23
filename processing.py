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
df.shape

with open('expert.txt') as f:
    lines = f.readlines()
    
expert_list = []

for line in lines:
    if line.rstrip():
        expert_list.append(ast.literal_eval(line))
        
df1 = pd.DataFrame(expert_list, columns=[['index']+list(df.columns)]).drop('index', axis=1)
df1.shape

df1 = df1.replace('wes','', regex=True).replace('wsh','', regex=True).replace('wsk','', regex=True)\
                                 .replace('shk','', regex=True).replace('hka','', regex=True)\
                                 .replace('wha','', regex=True)
df1 = df1.replace('+', True).replace('-', False).replace('+-', np.nan)

for col in df.columns:
    print('----', col, '----')
    print('------------------------\n')
    df_ = df.loc[df1[col].fillna(False).values][col]
    print(df_.describe())
    print('\nMedian:', df_.median())
    print('Mean:', df_.mean())
    print('Std:', df_.std())
    print('Min:', df_.min(), '\nMax:',df_.max(), '\n')
    
    
print('Median')
for col in df.columns:
#     print('----', col, '----')
    df_ = df.loc[df1[col].fillna(False).values][col]
    print(round(df_.median()/180,3))
    
print('Median+Std')
for col in df.columns:
#     print('----', col, '----')
    df_ = df.loc[df1[col].fillna(False).values][col]
    print(round((df_.median()+df_.std())/180,3))
    
print('Median+2xStd')
for col in df.columns:
#     print('----', col, '----')
    df_ = df.loc[df1[col].fillna(False).values][col]
    print(round((df_.median()+2*df_.std())/180,3))
