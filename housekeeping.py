import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np


# This was created in an attempt to fix a bug.
# Did not fix that bug.
# Seems useful anyway, but might not be needed.
def strip(data_df):
    # Checking for empty data
    data_df['PARTY'].replace('', np.nan, inplace=True)
    data_df.dropna(subset=['PARTY'], inplace=True)

    data_df['latest'].replace('', np.nan, inplace=True)
    data_df.dropna(subset=['latest'], inplace=True)

    return data_df
