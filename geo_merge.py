import pandas as pd
import os
import paths


# Looks like in the election_results process, some of the FIPS codes are getting condensed (01 becomes 1).
# Not sure if it matters that much, but is the sort of the thing that could bite you in the butt later.

# Merge Steps:
#     glue_data + election_results = political.csv (maybe just handcraft this part)
#     + covid_data = covid_political.csv
#     + geo_shape = debug.csv (good luck opening this in a spreadsheet program)

def geo_merge(detail_level, path_object, covid_df, shape_df):
    glue_df = pd.read_csv(path_object.glue_file)
    election_results_df = pd.read_csv(path_object.election_results)
    # TODO: county merging with STUSPS - not unique, problem?
    #  make sure one stays named the same and delete the other column?
    print("Merging glue data to election results...")
    if detail_level == "county":
        merged_political_df = pd.merge(glue_df, election_results_df, how='left',
                                       left_on=['COUNTY_NAME', 'STUSPS', 'FIPS'],
                                       right_on=['COUNTY_NAME', 'STUSPS', 'FIPS'])
    else:
        merged_political_df = pd.merge(glue_df, election_results_df, how='left',
                                       left_on=['STATE_FP', 'STUSPS', 'STATE_NAME', 'STATENS'],
                                       right_on=['STATE_FP', 'STUSPS', 'STATE_NAME', 'STATENS'])
    merged_political_df.to_csv(path_object.political_file)
    print(str(path_object.political_file))

    print("Freeing memory: glue_df, election_results_df")
    del glue_df
    del election_results_df

    print("Merging covid data to election results...")
    if detail_level == "county":
        # County election_results data: STATE_FP, COUNTY_FP, COUNTY, FIPS, COUNTY_NAME, STUSPS
        # County election results: STATE_NAME, STUSPS, COUNTY_NAME, FIPS, PARTY
        # Covid 19 Cases by County: fips (odd format: 1001.0), state (name), county (name)
        political_covid_df = pd.merge(covid_df, merged_political_df, how='left',
                                      left_on=['county'],
                                      right_on=['COUNTY_NAME'])
    else:
        # state election_results: COVID 19 Cases by State: State (name)
        political_covid_df = pd.merge(covid_df, merged_political_df, how='left',
                                      left_on=['State'],
                                      right_on=['STATE_NAME'])
    political_covid_df.to_csv(path_object.covid_political_file)
    print(str(path_object.covid_political_file))

    print("Freeing memory: covid_df, merged_political_df")
    del covid_df
    del merged_political_df

    print("Merging shape file to covid data...")
    if detail_level == "county":
        # cb_2019_us_county_5m.shp
        # keys:
        # ['STATEFP', 'COUNTYFP', 'COUNTYNS', 'AFFGEOID', 'GEOID', 'NAME', 'LSAD', 'ALAND', 'AWATER', 'geometry']
        merged_shape_df = shape_df.set_index('NAME').join(political_covid_df.set_index('COUNTY_NAME'))

        # merged_shape_df = pd.election_results(political_covid_df, shape_df, how='left',
        #                            left_on=['fips', 'county', 'state'],
        #                            right_on=['FIPS', 'COUNTY_NAME', 'STATE_NAME'])
    else:
        # cb_2019_us_state_5m.shp
        # keys:
        # ['STATEFP', 'STATENS', 'AFFGEOID', 'GEOID', 'STUSPS', 'NAME', 'LSAD', 'ALAND', 'AWATER', 'geometry']
        # drop conflicting rows
        political_covid_df = political_covid_df.drop(['STATENS'], axis=1)
        merged_shape_df = shape_df.set_index('STUSPS').join(political_covid_df.set_index('STUSPS'))
        # join works, election_results produces qix lines instead of usa shape

    merged_shape_df.to_csv(path_object.debug_file)
    print(str(path_object.debug_file))

    print("Freeing memory: shape_df, political_covid_df")
    del shape_df
    del political_covid_df

    return merged_shape_df
