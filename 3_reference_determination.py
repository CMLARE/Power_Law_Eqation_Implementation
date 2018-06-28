import pandas as pd
import numpy as np

df=pd.read_csv('new_dataset.csv')

#getting the mean of PRmin and PRmax, append the results as a new 'avg' column
df['avg']= df[['PRmin','PRmax']].mean(axis=1)

#delete the values in the 'avg' column if the time interval is not dry
def checkDry(x):
    if (x[0]=="Dry"):
        return x[1]
    else:
        return

df['avg']=df[['Wet/Dry','avg']].apply(checkDry, axis=1)

print(df)


