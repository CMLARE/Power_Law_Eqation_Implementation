import pandas as pd
import numpy as np


alp= 0.33 #default value
Aa = 2.3 #default value

df=pd.read_csv('new_dataset.csv')

ab=pd.read_csv('kRPowerLawData.csv')
ab=ab.sort_values('f')

def heaviside(A,Aa):
    if (A-float(Aa))<0:
        return 0
    else:
        return 1

def find_Rmin(Amin,Aa,L,a,b):
    return float(a)*(((Amin-float(Aa))/float(L))*(heaviside(Amin,Aa)))**float(b)

def find_Rmax(Amax,Aa,L,a,b):
    return float(a) * (((Amax - float(Aa)) / float(L)) * (heaviside(Amax, Aa))) ** float(b)


for index, row in df.iterrows():
    Amin = float(row['PRAvg'])-float(row['PRmax']) # 'PRavg' ---> 'PRref'
    Amax = float(row['PRAvg'])-float(row['PRmin']) # 'PRavg' ---> 'PRref'
    freq= float(row['Frequency'].split('.')[0].replace(',',''))/1000

    #getting the values for a and b from the table
    subtract = lambda x: abs(x - freq)
    temp_ab=ab
    temp_ab['f'] = temp_ab.f.astype(float)
    temp_ab['f']=temp_ab['f'].map(subtract)

    #select using index
    temp_ab=temp_ab.set_index(['f'])
    temp_ab.sort_index(inplace=True)

    #print(temp_ab.iloc[0])
    a = (temp_ab.iloc[0])['a']
    b = (temp_ab.iloc[0])['b']

    L=row['PathLength']

    Rmin= find_Rmin(Amin,Aa,L,a,b)
    Rmax= find_Rmax(Amax,Aa,L,a,b)

    R= alp*Rmax + (1-alp)*Rmin

    df['R']=R

print (df)
df.to_csv('R_output.csv',index=False)



