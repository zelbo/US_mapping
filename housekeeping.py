import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np


# Remove Guam, American Samoa, etc.
# Puerto Rico, U.S. Virgin Islands, Guam, Northern Mariana Islands, American Samoa.
# TODO: still an island chain in the upper left portion of the map
# remove these, or start getting data for them and create map insets?
# is there a cleaner way to do this? maybe add an "is_territory" column in the merge_glue-data step and strip on that?
def strip(data_df):
    # Checking for empty data
    data_df['PARTY'].replace('', np.nan, inplace=True)
    data_df.dropna(subset=['PARTY'], inplace=True)

    data_df['latest'].replace('', np.nan, inplace=True)
    data_df.dropna(subset=['latest'], inplace=True)

    # cleaned_data_df = data_df[data_df.PARTY != ""]
    # cleaned_data_df = cleaned_data_df[cleaned_data_df.latest != 0]
    return data_df
