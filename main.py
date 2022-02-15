################################################################################
# PROJECT: Find cities within 50km buffer zone around river mouths' centroids ##
# and make a ranking according to their populations.                          ##
# ##############################################################################
# AUTHOR                                                                      ##
# created by Piotr Stachyra on 15.02.2022                                     ##
################################################################################
# DATA (data folder)                                                          ##
# Retrieved from: https://www.naturalearthdata.com/                           ##
################################################################################


import inspect
import time
import sys

from readData import obtainGeoDataFrames
from visualizeLayers import plotPreview, visualizeRankedCities
from createBuffer import unifyCRS, createCoastlineBuffer
from findRiverMouths import findRiverMouthsCentroids, createRiverMouthBuffer
from rankCities import rankCities

def main():

    # Usage details
    if len(sys.argv) != 3:
        print("[ i ] Usage: %s <Project CRS Projection ESPG code> <Buffer radius in meters>\n[ i ] Example: ./main.py 4087 50000" % sys.argv[0])
        sys.exit(0)

    # set variables for CRS and buffer
    try:
        PROJECTCRS = int(sys.argv[1])
        BUFFERSIZE = float(sys.argv[2])
    except Exception as ex:
        print("[ ! ] Error: could not process command line arguments.\n[ ! ] Exception message: %s\nFunction: %s" % (ex, inspect.stack()[0][3]))
        sys.exit(-1)

    # measure program's performance
    start = time.perf_counter()

    # all geodataframes from the directory containing ZIP files
    # for different layers
    all_gdfs = obtainGeoDataFrames("data")

    # assigning the data structures to 4 layers of interest:
    # - the continents (land)
    # - the ocean (ocean)
    # - rivers (and lakes)
    # - cities
    land = all_gdfs[0]
    ocean = all_gdfs[1]
    cities = all_gdfs[2]
    rivers_lakes = all_gdfs[3]

    # removing all objects of internal waters except for rivers
    rivers = rivers_lakes[rivers_lakes["featurecla"] == "River"]

    # plot the global preview for all rivers, cities. In the context of land
    # (ocean is assumed to be a blank space of NULL)
    # the output is directed to 'visualizations' folder
    plotPreview(rivers, cities, land, "visualizations", show_preview=False)

    land_projected, cities_projected, rivers_projected, ocean_projected = unifyCRS(PROJECTCRS, land, cities, rivers, ocean)

    # buffer of 50km radius
    buffer_gdf = createCoastlineBuffer(land_projected, BUFFERSIZE)

    # extract cities within the buffer
    # conduct a spatial join between two layers based on their spatial relationship:
    # check if buffer contains a city polygon/multipolygon: identify these cities
    cities_within_buffer = buffer_gdf.sjoin(cities_projected, predicate="contains")

    # find river mouths: linestrings of intersection between ocean multipolygon and rivers' linestrings and
    # multilinestrings.
    river_mouth_centroids = findRiverMouthsCentroids(ocean_projected, rivers_projected)
    # make a buffer around river mouth centroids (50km radius), use project's CRS
    river_mouths_buffers = createRiverMouthBuffer(river_mouth_centroids, BUFFERSIZE, PROJECTCRS)

    # rank the cities which are located within the buffer zone around river mouths centroids according to
    # their population size.
    cities = rankCities(river_mouths_buffers, cities_projected)
    # plot a map containing these cities
    visualizeRankedCities(cities, river_mouths_buffers, rivers_projected, land_projected, "visualizations")

    # measure program's performance
    finish = time.perf_counter()
    time_delta = finish - start
    print("Program finished. Execution time: %f %s." % (time_delta, "second" if time_delta == 1 else "seconds"))
    print("The outputs have been saved to: visualizations and cities_rank directories.")

if __name__ == "__main__":
    main()