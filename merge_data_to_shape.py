# TODO: combine the other merge steps into one script
# merge steps:
#   add glue data to election results.
#   combine that with the covid data.
#   splice that onto the shape data.

def merge(shape_df, data_df):
    # merge glue data to dataframe
    merged_df = shape_df.set_index('STATE').join(data_df.set_index('STUSPS'))
    print("Merged dataframe preview:")
    print(merged_df.head())
    print(merged_df.columns)
    return merged_df
