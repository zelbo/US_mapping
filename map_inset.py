import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import os


# Puerto Rico, U.S. Virgin Islands, Guam, Northern Mariana Islands, American Samoa.
# also US minor outlying islands
# AK, HI, GU, MP, AS, PR, VI, UM - create constants or enum or something?
# TODO: still an island chain in the upper right portion of the map
# remove territories, or start getting data for them and create map insets?
# is there a cleaner way to do this? maybe add an "is_territory" column in the merge_glue-data step and strip on that?
# do we want to split the map, resize and move things, then re-merge the dataframe,
# or should we just resize and move them then plot each part individually?
def create_insets(shape_df):
    # TODO: parameters {optional}: shape, {add frames = true}, {include territories = true}
    include_territories = True
    # -Split-
    alaska_df = shape_df[shape_df['STATE'] == 'AK']
    hawaii_df = shape_df[shape_df['STATE'] == 'HI']
    puerto_rico_df = shape_df[shape_df['STATE'] == 'PR']
    virgin_islands_df = shape_df[shape_df['STATE'] == 'VI']
    guam_df = shape_df[shape_df['STATE'] == 'GU']
    mariana_islands_df = shape_df[shape_df['STATE'] == 'MP']
    american_samoa_df = shape_df[shape_df['STATE'] == 'AS']
    minor_outlying_islands_df = shape_df[shape_df['STATE'] == 'UM']

    # Contiguous US (Lower 48)
    shape_df = shape_df[shape_df['STATE'] != 'AK']
    shape_df = shape_df[shape_df['STATE'] != 'HI']
    shape_df = shape_df[shape_df['STATE'] != 'PR']
    shape_df = shape_df[shape_df['STATE'] != 'VI']
    shape_df = shape_df[shape_df['STATE'] != 'GU']
    shape_df = shape_df[shape_df['STATE'] != 'MP']
    shape_df = shape_df[shape_df['STATE'] != 'AS']
    shape_df = shape_df[shape_df['STATE'] != 'UM']

    # -Resize-
    # should automatically refer to geo_df.geometry, but maybe we need to specify just in case?
    # Shrink Alaska, maybe upscale the rest a bit?
    alaska_scale_factor_x = 0.01
    alaska_scale_factor_y = 0.01
    alaska_scale_factor_z = 0.0
    alaska_df.geometry.scale(alaska_scale_factor_x, alaska_scale_factor_y, alaska_scale_factor_z, 'center')
    island_scale_factor = 1.25

    # -Move-
    alaska_offset_x = 0.0
    alaska_offset_y = 0.0
    alaska_offset_z = 0.0
    alaska_df.geometry.translate(alaska_offset_x, alaska_offset_y, alaska_offset_z)

    hawaii_offset_x = 0.5
    hawaii_offset_y = 0.5
    hawaii_offset_z = 0.0
    hawaii_df.translate(hawaii_offset_x, hawaii_offset_y, hawaii_offset_z)

    # -Merge-
    shape_df = shape_df.append(alaska_df)
    shape_df = shape_df.append(hawaii_df)

    # if include territories:
    if include_territories:
        shape_df = shape_df.append(puerto_rico_df)
        shape_df = shape_df.append(virgin_islands_df)
        shape_df = shape_df.append(guam_df)
        shape_df = shape_df.append(mariana_islands_df)
        shape_df = shape_df.append(american_samoa_df)
        shape_df = shape_df.append(minor_outlying_islands_df)

    return shape_df
