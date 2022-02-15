import geopandas as gpd
import inspect
import sys

def findRiverMouth(ocean_gdf, rivers_gdf):
    """Returns a GeoSeries containing lineStrings which indicate
    a boundary where river falls into the ocean."""

    try:
        # find the linestrings by intersecting the ocean multipolygon with the rivers LineStrings (the GeoSeries structure)
        river_mouths_multilinestring = ocean_gdf["geometry"].unary_union.intersection(rivers_gdf["geometry"].unary_union)
        # create a GeoDataFrame from the multilinestring object
        river_mouths = gpd.GeoDataFrame(river_mouths_multilinestring)
        river_mouths.columns = ["geometry"]
        # simplify the data structure: obtain a GeoSeries using the geometry column
        # of the GeoDataFrame
        # overwrite the previous structure, GC will take care of the dangling object
        river_mouths = gpd.GeoSeries(river_mouths["geometry"])
    except Exception as ex:
        print("[ ! ] Error.\n[ ! ] Exception message: %s\nFunction: %s" % (ex, inspect.stack()[0][3]))
        sys.exit(-1)

    return river_mouths

def findRiverMouthsCentroids(ocean_gdf, rivers_gdf):
    """Returns a GeoSeries containing Point geometries for the
    river mouths centroids.
    Expects ocean GeoDataFrame and rivers GeoDataFrame objects."""

    try:
        # use the function for fining river's boundary at its mouth.
        river_mouths = findRiverMouth(ocean_gdf, rivers_gdf)
    except Exception as ex:
        print("[ ! ] Error.\n[ ! ] Exception message: %s\nFunction: %s" % (ex, inspect.stack()[0][3]))
        sys.exit(-1)

    return river_mouths.centroid

def createRiverMouthBuffer(river_mouth_centroids, buffer_radius, epsg_crs_projection_code):
    """Returns a GeoDataFrame containing data on the Polygon geometries
    which constitute the buffer zones around river mouths centroids.
    Expects a GeoSeries of the centroids and a buffer radius."""

    try:
        river_mouth_buffers_gdf = gpd.GeoDataFrame(river_mouth_centroids.buffer(buffer_radius))
        river_mouth_buffers_gdf.columns = ["geometry"]
        river_mouth_buffers_gdf = river_mouth_buffers_gdf.set_crs(f"epsg:{epsg_crs_projection_code}")
    except Exception as ex:
        print("[ ! ] Error.\n[ ! ] Exception message: %s\nFunction: %s" % (ex, inspect.stack()[0][3]))
        sys.exit(-1)

    return river_mouth_buffers_gdf
