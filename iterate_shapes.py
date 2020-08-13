import os
import geopandas as gpd
import matplotlib.pyplot as plt


# Summarize: Count rows of data, size of files, name of shapefile
# Open file to dataframe
# Save csv of headers & three rows of data
# Save figure image
# Show plot
# Find source and license for each shapefile

# TODO: save map.png to an 'images' directory

def iterate_shapes():
    # TODO: variable names are a little convoluted
    #  make it more clear what is going on here.
    relative_path = os.path.dirname(__file__)
    data_path = os.path.join(relative_path, "data")
    image_path = os.path.join(relative_path, "images")
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    shape_path = os.path.join(data_path, "shapes")
    report_path = os.path.join(data_path, "reports")
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    summary_file = os.path.join(data_path, "summary.txt")

    # TODO: is there a better way to reset summary file? move the file pointer back to 0?
    summary = open(summary_file, 'w+')
    summary.close()

    # Recursively check whole directory?
    # for (dirpath, dirnames, filenames) in os.walk(shape_path):
    #    file_list.extend(filenames)
    #    break
    file_list = []
    for file in os.listdir(shape_path):
        if file.endswith(".shp"):
            shape_file = os.path.join(shape_path, file)
            print(os.path.join(shape_path, file))
            file_list.extend(file)

            # create report file for each shape file
            report_file = os.path.join(report_path, file + '.txt')
            report = open(report_file, 'w+')

            file_size = os.stat(shape_file).st_size
            file_path = os.path.join(shape_path, file)
            shape_df = gpd.read_file(file_path)
            file_keys = shape_df.keys()
            file_columns = shape_df.columns
            file_head = shape_df.head(3)
            file_shape = shape_df.shape
            file_memory = shape_df.memory_usage()
            file_length = len(shape_df)

            summary_data = "file name: " + file + "\n" + "file size: " + str(file_size) + " bytes" + "\n"
            summary_data = summary_data + "\n" + "keys: " + "\n" + str(file_keys) + "\n"
            summary_data = summary_data + "\n" + "columns: " + "\n" + str(file_columns) + "\n"
            summary_data = summary_data + "\n" + "head: " + "\n" + str(file_head) + "\n"
            summary_data = summary_data + "\n" + "length: " + "\n" + str(file_length) + "\n"
            summary_data = summary_data + "\n" + "shape: " + "\n" + str(file_shape) + "\n"
            summary_data = summary_data + "\n" + "memory usage in bytes: " + "\n" + str(file_memory) + "\n"
            report.write(summary_data)
            report.close()

            # create shape file entry in master summary file
            # keys, column, head, length
            mini_summary_data = "Summary for: " + file + "\n" + "file size: " + str(format_bytes(file_size)) + "\n"
            mini_summary_data = mini_summary_data + "\n" + "keys: " + "\n" + str(file_keys) + "\n"
            mini_summary_data = mini_summary_data + "\n" + "columns: " + "\n" + str(file_columns) + "\n"
            mini_summary_data = mini_summary_data + "\n" + "head: " + "\n" + str(file_head) + "\n"
            mini_summary_data = mini_summary_data + "\n" + "length: " + "\n" + str(file_length) + "\n" + "\n"

            summary = open(summary_file, 'a+')
            summary.write(mini_summary_data)
            summary.close()
            # image_file = os.path.join(image_path, file + '.png')
            my_size = str(format_bytes(file_size))
            map_save(file, image_path, my_size, shape_df)

    print(file_list)

    return file_list


# From The Documentation:
# Do not use os.linesep as a line terminator when writing files opened in text mode
# (the default); use a single '\n' instead, on all platforms.

def format_bytes(size):
    # 2**10 = 1024
    power = 2 ** 10
    n = 0
    power_labels = {0: '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n] + 'bytes'


def map_save(file_name, image_file, my_size, shape_df):
    # TODO: extract magic numbers
    fig, ax = plt.subplots(1, figsize=(6, 2))
    ax.axis('off')
    map_title = str(file_name)
    ax.set_title(map_title.title(), fontdict={'fontsize': '12', 'fontweight': '1'})
    ax.annotate(my_size, xy=(0.1, .08),
                xycoords='figure fraction',
                horizontalalignment='left',
                verticalalignment='top',
                fontsize=12, color='#555555')

    fig.tight_layout()
    shape_df.plot(cmap='Greys', linewidth=0.8, ax=ax, edgecolor='0.8')

    map_name = map_title + ".png"
    map_name = map_name.replace(" ", "_")
    map_name = map_name.replace("/", "-")
    map_path = os.path.join(image_file, map_name)
    fig.savefig(map_path, dpi=300)

    fig.savefig(map_name, dpi=300)

    # plt.show()
    # Matplotlib gives you lots of freedom in how you save figures.
    # The code below will save the figure as a png,
    # but if you want to fiddle about some more with it in Illustrator you can also save as svg.
    # If you save as png, make sure to use a dpi of 200 or above.
    # Otherwise the map and text will look all blurry. Nobody wants that.
    # fig.savefig("map_export.png", dpi=300)

    return
