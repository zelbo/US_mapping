import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt

# -Getting the data-
# Shapefiles require all the files (.dbf, .shx, etc.) be in the same folder with it.
# Geopandas can work with zip files, but if there are more than one shape file in that zip,
# you must specify wich one you are using.
base_file_path = "/home/rain/Projects/US_mapping"
#shape_file_path = "/shapefiles/tl_2019_us_county.shp"
shape_file_path = "/shapefiles/s_11au16.shp"
merged_political_path = "/merged_political.csv"
cases_by_county_path = "/covid-19-usa-by-state-master/COVID-19-Cases-USA-By-County.csv"
cases_by_state_path = "/covid-19-usa-by-state-master/cases_by_state_cleaned.csv"
deaths_by_county_path = "/covid-19-usa-by-state-master/COVID-19-Deaths-USA-By-County.csv"
deaths_by_state_path = "/covid-19-usa-by-state-master/COVID-19-Deaths-USA-By-State.csv"
election_by_state_path = "/state_results.csv"
merge_state_path = "/merge_state.csv"
save_df_as_csv_path = "/dataframe.csv"
#save_merged_political_path = "/merged_political.csv"


# The map.
shape_df = gpd.read_file(base_file_path + shape_file_path)
print("Shape file preview:")
print(shape_df.head())
print(shape_df.columns)
# Remove Guam, American Samoa, etc.
#us_50_states_df = shape_df.drop([54, 55, 56])
# filter rows for year 2002 using  the boolean expression
#>gapminder_2002 = gapminder[gapminder.year.eq(2002)]
#>print(gapminder_2002.shape)

us_50_states_df = shape_df[shape_df.STATE != "GU"]
us_50_states_df = us_50_states_df[us_50_states_df.STATE != "MP"]
us_50_states_df = us_50_states_df[us_50_states_df.STATE != "AS"]
us_50_states_df = us_50_states_df[us_50_states_df.STATE != "PR"]
us_50_states_df = us_50_states_df[us_50_states_df.STATE != "VI"]



#print(shape_df.drop(index=['51', '52', '53', '54', '55']))
#contiguous_us_df = merged_df[merged_df['STUSPS'] != 'AK']
#us_50_states_df = shape_df[shape_df['STUSPS'] != 'GU']
#us_50_states_df = us_50_states_df[us_50_states_df['STUSPS'] != 'MP']
#us_50_states_df = us_50_states_df[us_50_states_df['STUSPS'] != 'AS']
#us_50_states_df = us_50_states_df[us_50_states_df['STUSPS'] != 'PR']
#us_50_states_df = us_50_states_df[us_50_states_df['STUSPS'] != 'VI']

#shape_df.plot()
# us_map = us_50_states_df.plot()
#us_map = us_50_states_df.plot()

# to dig into the data and check what is where
#csv_file = base_file_path + save_df_as_csv_path
#us_50_states_df.to_csv(csv_file)

# The data
data_df = pd.read_csv(base_file_path + merged_political_path)
print("Data file preview:")
print(data_df.head())
print(data_df.columns)

#merge_df = pd.read_csv(base_file_path + merge_state_path)
#merged_data_df = data_df.set_index('State').join(merge_df.set_index('STATE_NAME'))
#merged_political_df = merged_data_df.merge(election_results_df, on='STUSPS', how='outer')
#merged_political_df = merged_data_df.set_index('STUSPS').join(election_results_df.set_index('STUSPS'))
#print("Merged data preview:")
#print(merged_data_df.head())
#print(merged_data_df.columns)
#csv_file = base_file_path + save_merged_political_path
#merged_political_df.to_csv(csv_file)


#df_a.merge(df_b, on='mukey', how='left')
merged_df = us_50_states_df.set_index('STATE').join(data_df.set_index('STUSPS'))
#merged_df = data_df.merge(shape_df, on='STUSPS', how='outer')
print("Merged dataframe preview:")
print(merged_df.head())
print(merged_df.columns)

red_states_df = merged_df[merged_df.PARTY.eq('R')]
blue_states_df = merged_df[merged_df.PARTY.eq('D')]


# Split out Alaska and Hawaii.
#alaska_df = merged_df[merged_df['STUSPS'] == 'AK']
#hawaii_df = merged_df[merged_df['STUSPS'] == 'HI']
#contiguous_us_df = merged_df[merged_df['STUSPS'] != 'AK']
#contiguous_us_df = merged_df[merged_df['STUSPS'] != 'HI']

# gdf.geometry
# Resize Alaska
#scale_factor_x = 0.4
#scale_factor_y = 0.4
#alaska_df.scale(scale_factor_x, scale_factor_y, 0.0, 'center')

# Move Alaska and Hawaii
#alaska_offset_x = 0.0
#alaska_offset_y = -140.0
#alaska_offset_z = 0.0

#hawaii_offset_x = 0.5
#hawaii_offset_y = 0.5
#hawaii_offset_z = 0.0

#alaska_df.translate(alaska_offset_x, alaska_offset_y, alaska_offset_z)
#hawaii_df.translate(hawaii_offset_x, hawaii_offset_y, hawaii_offset_z)

display_value = 'latest'

color_min = 120
color_max = 220

# create figure and axes for Matplotlib
# This looks strange to me, but I guess it's legal python.
# TODO: extract magic numbers
#ax = us_map.get_figure()
fig, ax = plt.subplots(1, figsize=(6, 2))
ax.axis('off')
ax.set_title("Testing State map US", fontdict={'fontsize': '25', 'fontweight': '3'})
# ax.annotate("Source: London Datastore, 2014", xy=(0.1, .08),
#            xycoords='figure fraction', horizontalalignment='left',
#            verticalalignment='top', fontsize=12, color='#555555')

# Create colorbar as a legend
# TODO: add second colorbar
sm = plt.cm.ScalarMappable(cmap='Greys', norm=plt.Normalize(vmin=color_min, vmax=color_max))

# empty array for the data range
sm._A = []
# add the colorbar to the figure
cbar = fig.colorbar(sm)

# create map
# TODO: extract magic numbers
# ax=ax? that can't be right. refactor.
#entire_us_df.plot(column=display_value, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')
#entire_us_df.plot(display_value, cmap='Blues', linewidth=0.8, ax=ax, markeredgecolor='0.8', markeredgewidth=1)

# to dig into the data and check what is where
#csv_file = base_file_path + save_df_as_csv_path
#entire_us_df.to_csv(csv_file)

fig.tight_layout()
#us_50_states_df.plot
us_50_states_df.plot(cmap='Greys', linewidth=0.8, ax=ax, edgecolor='0.8')
red_states_df.plot(display_value, ax=ax, cmap='Reds')
blue_states_df.plot(display_value, ax=ax, cmap='Blues')
# Save the image (is this the right place for this operation?)
# TODO: error handling - what happens if the file exists? overwrite? rename?
# fig.savefig("map_export.png", dpi=300)
# Show the map
fig.tight_layout()

plt.show()

# Matplotlib gives you lots of freedom in how you save figures.
# The code below will save the figure as a png,
# but if you want to fiddle about some more with it in Illustrator you can also save as svg.
# If you save as png, make sure to use a dpi of 200 or above.
# Otherwise the map and text will look all blurry. Nobody wants that.
# fig.savefig("map_export.png", dpi=300)
