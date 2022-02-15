import inspect
import os
import sys

def rankCities(river_mouths_buffers_gdf, coastal_cities_gdf):
    """Returns a GeoDataFrame - a ranking of cities within the buffer zone around river mouths centroids.
    Expects the river mouths buffers GeoDataFrame, cities of interest GeoDataFrame."""

    try:
        # perform the spatial join to include the cities within the buffer zone
        cities_in_buffer = river_mouths_buffers_gdf.sjoin(coastal_cities_gdf, predicate="contains")
        # limit the GeoDataFrame contents to the city name and city population
        cities_in_buffer = cities_in_buffer[["NAME", "POP2020", "geometry"]]
        # order the cities in descending order (population)
        ranked_cities = cities_in_buffer.sort_values("POP2020", ascending=False)

        # make an output report in CSV file format
        if not os.path.isdir("cities_rank"):
            os.mkdir("cities_rank")
        ranked_cities.to_csv("cities_rank/cities.csv")
        ranked_cities.to_file("cities_rank/cities.gpkg", driver="GPKG", layer="cities")
    except Exception as ex:
        print("[ ! ] Error.\n[ ! ] Exception message: %s\nFunction: %s" % (ex, inspect.stack()[0][3]))
        sys.exit(-1)

    return ranked_cities