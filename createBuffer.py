import geopandas as gpd
import inspect
import sys

def unifyCRS(epsg_code, *args):
    """Variadic function. Takes a mandatory parameter of a CRS projection's EPSG code.
    This is the CRS which will be assigned to the data.
    The additional arguments (va_list, args) should be GeoDataFrames in order to assign the CRS."""

    # A list to store the copies of geodfs
    # with CRS adjusted.
    try:
        changed_crs_gdfs = []
        for arg in args:
            new_crs = arg.to_crs(epsg=epsg_code)
            changed_crs_gdfs.append(new_crs)
    except Exception as ex:
        print("[ ! ] Error.\n[ ! ] Exception message: %s\nFunction: %s" % (ex, inspect.stack()[0][3]))
        sys.exit(-1)

    return changed_crs_gdfs


def createCoastlineBuffer(land_gdf_projected, buffer_radius):
    """This function creates a buffer around the coastline.
    Expects data on lands multipolygon layer in a projected CRS context (land_gdf_projected)
    and the radius of the buffer which is expressed in UoM for the projection (buffer_radius).
    Returns a dataframe - a buffer zone around coastlines with the buffer's radius
    expressed in the projection's UoM (usually meters)."""

    try:
        # get the EPSG code of the CRS used by the provided geodataframe
        crs_epsg_code = int(str(land_gdf_projected.crs).split(":")[1])
        # create the buffer area
        coastline_buffer = land_gdf_projected["geometry"].boundary.buffer(buffer_radius)
        # turn the data on the buffer to a geodataframe
        coastline_buffer_gdf = gpd.GeoDataFrame(coastline_buffer)
        # change the only column to 'geometry'
        coastline_buffer_gdf.columns = ["geometry"]
        # ensure that the buffer area has a projected CRS, the same
        # as for the input geodataframe
        coastline_buffer_gdf = coastline_buffer_gdf.to_crs(epsg=crs_epsg_code)

    except Exception as ex:
        print("[ ! ] Error.\n[ ! ] Exception message: %s\nFunction: %s" % (ex, inspect.stack()[0][3]))
        sys.exit(-1)

    return coastline_buffer_gdf