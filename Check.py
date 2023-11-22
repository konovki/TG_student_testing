import numpy as np
import pandas as pd
import os

pd.set_option('display.max_rows', None)
while True:
    names = os.listdir('./')
    csv_files = []
    for name in names:
        if 'csv' in name:
            csv_files.append(name)
    for i in range(len(csv_files)):
        print(i,csv_files[i])
    print('choose file')
    file = input()
    if file == 'exit':
        break
    else:
        df = pd.read_csv(f'./{csv_files[int(file)]}')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        for name in np.unique(np.array(df['name'])):
    
            print(df[df['name']==name])
#Булдакова4
