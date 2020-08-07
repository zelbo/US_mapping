import pandas as pd
import os

relative_path = os.path.dirname(__file__)
data_path = os.path.join(relative_path, "data")
# merge_path = os.path.join(data_path, "merge")

county_merged_file = os.path.join(data_path, "county_merged_political.csv")
state_merged_file = os.path.join(data_path, "state_merged_political.csv")


# Looks like in the merge process, some of the FIPS codes are getting condensed (01 becomes 1).
# Not sure if it matters that much, but is the sort of the thing that could bite you in the butt later.
def glue(include_counties, glue_df, election_results_df):
    if include_counties:
        # county merge:
        merged_df = pd.merge(glue_df, election_results_df, how='left',
                             left_on=['COUNTY_NAME', 'STUSPS', 'FIPS'],
                             right_on=['COUNTY_NAME', 'STUSPS', 'FIPS'])
        merged_df.to_csv(county_merged_file)
    else:
        # state merge:
        merged_df = pd.merge(glue_df, election_results_df, how='left',
                             left_on=['STATE_FP', 'STUSPS', 'STATE_NAME', 'STATENS'],
                             right_on=['STATE_FP', 'STUSPS', 'STATE_NAME', 'STATENS'])
        merged_df.to_csv(state_merged_file)
    return merged_df
