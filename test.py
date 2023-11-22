import numpy as np
import pandas as pd
pd.set_option('display.max_rows', None)
df = pd.read_csv('./df_2023_09_27_11_38_49_465232.csv')
print(df)
for name in np.unique(np.array(df['name'])):
    print('student', name)
    print(df[df['name']==name])
#Булдакова4