import pandas as pd
import geopandas as gpd
import os
import display_map
import map_inset
import merge_data_to_shape
import housekeeping
import add_geo_glue


# -Folders-
relative_path = os.path.dirname(__file__)
data_path = os.path.join(relative_path, "data")
shape_path = os.path.join(data_path, "shapefiles")
covid_data_path = os.path.join(data_path, "covid")
debug_path = os.path.join(relative_path, "debug")
merge_path = os.path.join(data_path, "merge")

# -Files-
# TODO: use api to fetch updated covid data from trusted source
# TODO: create toggle for state or county views
# TODO: create toggle for deaths, active cases, new cases, or total cases (recovered + active)
# TODO: if merged doesn't exist, create merged
state_shapefile = os.path.join(shape_path, "s_11au16.shp")
state_datafile = os.path.join(data_path, "merged_political.csv")
# the things we've tweaked by hand, let's make scripts to do that
# automate more processes rather than do things in excel
debug_file = os.path.join(debug_path, "debug_data.csv")

# TODO: move some of this file IO stuff to a get_data function?
county_merged_file = os.path.join(data_path, "county_merged_political.csv")
state_merged_file = os.path.join(data_path, "state_merged_political.csv")
state_election_results = os.path.join(merge_path, "data/state_results.csv")
county_election_results = os.path.join(merge_path, "county_results.csv")
state_glue_file = os.path.join(merge_path, "state_glue.csv")
county_glue_file = os.path.join(merge_path, "county_glue.csv")

# TODO: start just using the actual latest column, don't manually edit the file to make a latest column
column_to_analyze = "latest"
# TODO: start using command line parameters
# default to just states
include_counties = False

shape_df = gpd.read_file(state_shapefile)
shape_df = map_inset.create_insets(shape_df)

data_df = pd.read_csv(state_datafile)

# TODO: merge all the merge functions into one script
if include_counties:
    # county scope
    try:
        merged_political_df = pd.read_csv(county_merged_file)
    except IOError:
        print("County merged political file doesn't exist: generating...")
        county_glue_df = pd.read_csv(county_glue_file)
        county_election_df = pd.read_csv(county_election_results)
        add_geo_glue.glue(include_counties, county_glue_df, county_election_df)
else:
    # state scope
    try:
        merged_political_df = pd.read_csv(state_merged_file)
    except IOError:
        print("State merged political file doesn't exist: generating...")
        state_glue_df = pd.read_csv(state_glue_file)
        state_election_df = pd.read_csv(state_election_results)
        add_geo_glue.glue(include_counties, state_glue_df, state_election_df)

merged_df = merge_data_to_shape.merge(shape_df, data_df)

merged_df = housekeeping.strip(merged_df)
# to dig into the data and check what is where
merged_df.to_csv(debug_file)

display_map.map_show(merged_df, column_to_analyze)
