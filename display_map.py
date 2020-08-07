import matplotlib.pyplot as plt


def map_show(combined_df, display_value):
    # display_value = 'latest'
    red_states_df = combined_df[combined_df.PARTY.eq('R')]
    blue_states_df = combined_df[combined_df.PARTY.eq('D')]

    color_min = 0
    color_max = 200000

    # create figure and axes for Matplotlib
    # This looks strange to me, but I guess it's legal python.
    # TODO: extract magic numbers
    # ax = us_map.get_figure()
    fig, ax = plt.subplots(1, figsize=(6, 2))
    ax.axis('off')
    ax.set_title("Testing State map US", fontdict={'fontsize': '25', 'fontweight': '3'})
    # ax.annotate("Source: London Datastore, 2014", xy=(0.1, .08),
    #            xycoords='figure fraction', horizontalalignment='left',
    #            verticalalignment='top', fontsize=12, color='#555555')

    # Create colorbar as a legend
    # TODO: add second colorbar?
    sm = plt.cm.ScalarMappable(cmap='Greys', norm=plt.Normalize(vmin=color_min, vmax=color_max))

    # empty array for the data range
    sm._A = []
    # add the colorbar to the figure
    # TODO: pycharm tells me cbar is not used - what did I do? Is this not needed anymore?
    cbar = fig.colorbar(sm)

    # create map
    # TODO: extract magic numbers
    # ax=ax? that can't be right. rename?

    fig.tight_layout()
    # us_50_states_df.plot
    combined_df.plot(cmap='Greys', linewidth=0.8, ax=ax, edgecolor='0.8')
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

    return

# if __name__ == '__main__':
#    map_show(combined_df, display_value)
