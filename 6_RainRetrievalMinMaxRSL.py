import numpy as np
import pandas as pd

def RainRetrievalMinMaxRSL(Data, kRPowerlawData,PRef):
    FrequencyLinks = Data.Frequency.unique()
    Data["a"] =  np.nan
    Data["b"] =  np.nan
    for i in range(FrequencyLinks.size):
        param = kRPowerlawData.loc[kRPowerlawData['f'] == FrequencyLinks[i]]
        Data.ix[Data['Frequency'] == FrequencyLinks[i], ['a','b']] = [param["a"],param["b"]]
    return Data


def MinMaxRSLToMeanR(Data, PRef):
    dataframe = Data[["DateTime", "Frequency", "a", "b", "Pmin", "Pmax", "PathLength"]]
    dataframe['Amin'] = PRef + dataframe['Pmax']
    dataframe['Amax'] = PRef - dataframe['Pmin']

    dataframe['Rmin'] = dataFrame["a"] * (dataFrame("Amin") / dataFrame("PathLength")) ^ dataFrame("b")
    dataframe['Rmax'] = dataFrame["a"] * (dataFrame("Amax") / dataFrame("PathLength")) ^ dataFrame("b")
    return dataFrame
