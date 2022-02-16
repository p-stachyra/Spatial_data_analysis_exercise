import inspect
import matplotlib.pyplot as plt
import os
import sys

def plotPreview(rivers_gdf, cities_gdf, land_gdf, output_directory, show_preview=False):
    try:
        # extract figure and axes
        fig, ax = plt.subplots(1, 1, figsize=(20, 30))

        # Plot rivers
        rivers_gdf.plot(ax=ax, markersize=0.1, alpha=0.5, color="blue")
        # Plot cities according to their size
        cities_gdf.plot(ax=ax, markersize=0.5, alpha=0.5, color="red")
        # Plot land
        land_gdf.plot(ax=ax, alpha=0.2, color="green")

        # check if visualizations directory exists
        # if not create it
        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)

        # title of the visualization
        plt.title("Cities and Rivers", size=20)
        plt.tight_layout()

        # check if Windows
        if (os.name == "nt"):
            plt.savefig(f"{output_directory}\\cities_rivers_global.PNG")
        # otherwise use forward slash
        else:
            plt.savefig(f"{output_directory}/cities_rivers_global.PNG")

        # if preview is selected to be show, display the plot
        if (show_preview):
            plt.show()

    except Exception as ex:
        print("[ ! ] Error.\n[ ! ] Exception message: %s\nFunction: %s" % (ex, inspect.stack()[0][3]))
        sys.exit(-1)

    # return exitcode
    return 0

def visualizeRankedCities(ranked_cities, river_mouths_buffer, rivers_projected_gdf, land_projected_gdf, output_directory, postfix):
    """Creates a visualization of the ranked cities which are within the river mouths buffers.
    Expects the ranked cities, river_mouths_buffers, rivers, land GeoDataFrames
    and the directory to store plots."""

    try:
        # extract figure and axes
        fig, ax = plt.subplots(figsize=(20, 30))

        rivers_projected_gdf.plot(ax=ax, markersize=0.1, alpha=0.3, color="blue")
        # Plot cities according to their size
        ranked_cities.plot(ax=ax, markersize=0.5, alpha=0.9, color="red")
        # plot buffers
        river_mouths_buffer.plot(ax=ax, markersize=0.5, alpha=0.4, color="yellow")
        # Plot land
        land_projected_gdf.plot(ax=ax, alpha=0.2, color="green")

        # check if visualizations directory exists
        # if not create it
        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)

        # title of the visualization
        plt.title("Ranked Cities", size=20)
        plt.tight_layout()

        # check if Windows
        if (os.name == "nt"):
            plt.savefig(f"{output_directory}\\ranked_cities_{str(postfix)}.PNG")
        # otherwise use forward slash
        else:
            plt.savefig(f"{output_directory}/ranked_cities_{str(postfix)}.PNG")

    except Exception as ex:
        print("[ ! ] Error.\n[ ! ] Exception message: %s\nFunction: %s" % (ex, inspect.stack()[0][3]))
        sys.exit(-1)