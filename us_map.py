import pandas as pd
import geopandas as gpd
import display_map
import map_inset
import geo_merge
import paths


# state or county
detail_level = "state"
# cases or deaths
data_option = "deaths"
# True or False
include_territories = False

path_object = paths.PathClass(detail_level, data_option)
print("Detail level: " + detail_level)
print("Data option: " + data_option)

# TODO: use api to fetch updated covid data from trusted source
# TODO: start using command line parameters
#  create toggle for state or county views
#  create toggle for deaths, active cases, new cases, or total cases (recovered + active)
# TODO: start just using the actual latest column, don't manually edit the file to make a latest column
#  find a way to get the date columns for this dynamically
#  make a list of the date headers and sort that?
if detail_level == "state":
    column_to_analyze = "7/18/20"
else:
    column_to_analyze = "2020-07-18"

# TODO: move this logic to the paths script?
if detail_level == "state":
    shape_df = gpd.read_file(path_object.state_shapefile)
    if data_option == "cases":
        covid_df = pd.read_csv(path_object.state_covid_cases_file)
    else:
        covid_df = pd.read_csv(path_object.state_covid_deaths_file)
else:
    shape_df = gpd.read_file(path_object.county_shapefile)
    if data_option == "cases":
        covid_df = pd.read_csv(path_object.county_covid_cases_file)
    else:
        covid_df = pd.read_csv(path_object.county_covid_deaths_file)

#print("Saving shape to csv: " + detail_level + "_shape_debug.csv")
#shape_df.to_csv(detail_level + "_shape_debug.csv")
print("Creating map insets (Alaska, Hawaii, US Territories)...")
shape_df = map_inset.create_insets(shape_df, detail_level, include_territories)
print("Merging data...")
merged_df = geo_merge.geo_merge(detail_level, path_object, covid_df, shape_df)
# TODO: delete housekeeping? if no politics, show grey. if no data, get data.
# merged_df = housekeeping.strip(merged_df)
print("Making map visualization...")
display_map.map_show(merged_df, detail_level, data_option, column_to_analyze, path_object)
