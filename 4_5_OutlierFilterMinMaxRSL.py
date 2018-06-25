import numpy as np
import pandas as pd


def OutlierFilterMinMaxRSL(data, PRef):
    data = data.fillna(method='bfill')

    mask = data.Pmin > PRef
    data.loc[mask, 'Pmin'] = PRef

    mask = data.Pmax > PRef
    data.loc[mask, 'Pmax'] = PRef
    return data