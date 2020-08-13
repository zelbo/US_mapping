import os


class PathClass:
    # -Folders-
    relative_path = os.path.dirname(__file__)
    debug_path = os.path.join(relative_path, "debug")
    data_path = os.path.join(relative_path, "data")
    image_path = os.path.join(relative_path, "images")
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    shape_path = os.path.join(data_path, "shapes")
    covid_path = os.path.join(data_path, "covid")
    election_results_path = os.path.join(data_path, "election_results")

    # -Files-
    # TODO: don't like this at all. How to declare a blank path?
    no_file = os.path.join(data_path, "")
    election_results = no_file
    glue_file = no_file
    political_file = no_file
    covid_political_file = no_file
    debug_file = no_file

    state_shapefile = no_file
    county_shapefile = no_file
    state_covid_cases_file = no_file
    state_covid_deaths_file = no_file
    county_covid_cases_file = no_file
    county_covid_deaths_file = no_file

    def __init__(self, detail_level, data_option):
        detail_covid = detail_level + "_covid_" + data_option
        PathClass.election_results = os.path.join(PathClass.election_results_path, detail_level + "_results.csv")
        PathClass.glue_file = os.path.join(PathClass.election_results_path, detail_level + "_glue.csv")
        PathClass.political_file = os.path.join(PathClass.data_path, detail_level + "_political.csv")
        PathClass.covid_political_file = os.path.join(PathClass.data_path, detail_covid + "_political.csv")
        PathClass.debug_file = os.path.join(PathClass.debug_path, detail_covid + "_debug_data.csv")

        PathClass.state_shapefile = os.path.join(PathClass.shape_path, "cb_2019_us_state_5m.shp")
        PathClass.county_shapefile = os.path.join(PathClass.shape_path, "cb_2019_us_county_5m.shp")
        PathClass.state_covid_cases_file = os.path.join(PathClass.covid_path, "COVID-19-Cases-USA-By-State.csv")
        PathClass.state_covid_deaths_file = os.path.join(PathClass.covid_path, "COVID-19-Deaths-USA-By-State.csv")
        PathClass.county_covid_cases_file = os.path.join(PathClass.covid_path, "COVID-19-Cases-USA-By-County.csv")
        PathClass.county_covid_deaths_file = os.path.join(PathClass.covid_path, "COVID-19-Deaths-USA-By-County.csv")
        return
