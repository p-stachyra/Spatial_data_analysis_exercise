import inspect
import os
import sys

def rankCities(river_mouths_buffers_gdf, coastal_cities_gdf, postfix):
    """Returns a GeoDataFrame - a ranking of cities within the buffer zone around river mouths centroids.
    Expects the river mouths buffers GeoDataFrame, cities of interest GeoDataFrame."""

    try:
        # perform the spatial join to include the cities within the buffer zone
        cities_in_buffer = river_mouths_buffers_gdf.sjoin(coastal_cities_gdf, predicate="contains")
        # limit the GeoDataFrame contents to the city name and city population
        cities_in_buffer = cities_in_buffer[["NAME", "POP2020", "geometry"]]
        cities_in_buffer_no_geom = cities_in_buffer[["NAME", "POP2020"]]
        # order the cities in descending order (population)
        ranked_cities = cities_in_buffer.sort_values("POP2020", ascending=False)
        ranked_cities_no_geom = cities_in_buffer_no_geom.sort_values("POP2020", ascending=False)

        # make an output report in CSV file format
        if not os.path.isdir("cities_rank"):
            os.mkdir("cities_rank")
        # encoding must be set to UTF-8-SIG to properly encode letters of other languages than English
        ranked_cities_no_geom.to_csv(f"cities_rank/cities_{str(postfix)}.csv", encoding="utf-8-sig")
        ranked_cities.to_file(f"cities_rank/cities_{str(postfix)}.gpkg", driver="GPKG", layer="cities")
    except Exception as ex:
        print("[ ! ] Error.\n[ ! ] Exception message: %s\nFunction: %s" % (ex, inspect.stack()[0][3]))
        sys.exit(-1)

    return ranked_cities