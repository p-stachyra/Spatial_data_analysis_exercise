import geopandas as gpd
import inspect
import os
import sys

from zipfile import ZipFile

# Allowing for read-from-ZIP functionality to read shapefiles quickly
def readFromZIP(zip_name, directory="data"):
    """This function reads data from a shapefile (shp format: geometries file)
    The function takes 2 parameters.
    It expects 1 mandatory parameter: the ZIP file's name. Assumes that the ZIPs are located in
    a directory data by default.
    Returns shapefile data in a GeoDataFrame format."""

    # obtains the current working directory absolute path
    current_path = os.getcwd()

    try:
        # compose the absolute path of the target ZIP file
        # if WINDOWS_NT is detected, the backslash is used
        if (os.name == "nt"):
            absolute_path = os.path.join(current_path, f"{directory}\\{zip_name}")
        # otherwise, forward slash is used for the absolute path
        else:
            absolute_path = os.path.join(current_path, f"{directory}/{zip_name}")

        # the operation itself

        # context manager for handling the ZIP file
        with ZipFile(absolute_path) as zh:
            # list the files in the compressed file
            for file in zh.namelist():
                # if shp format is found, operate on that ZIP
                if file[-3:] == "shp":
                    proper_structure = True

            # otherwise, return error message
            if not proper_structure:
                print(
                    "[ ! ] Could not determine if the contents required for reading a shapefile are available.\nSHP file format not found.\nFunction: %s" % inspect.stack()[0][3])
                sys.exit(-1)

            shapefile_data = gpd.read_file(absolute_path)

    except Exception as ex:
        print("[ ! ] Error occured while reading the data.\n[ ! ] Exception message: %s\nFunction: %s" % (ex, inspect.stack()[0][3]))
        sys.exit(-1)

    # If the operation was performed successfully, the data from the read shapefile are returned.
    return shapefile_data

# a helper function
def retrieveAllZIPs(directory="data"):
    """This generator retreives all ZIP files' names in the provided directory.
    An optional argument for the directory containing ZIPs can be provided,
    otherwise the default is data."""
    for file in os.listdir(directory):
        if file[-3:].lower() == "zip":
            yield file

# reading the data from all sources
def obtainGeoDataFrames(directory="data"):
    """This function takes 1 optional argument - the directory name can be provided.
    By default it is 'data' directory.
    Stores geodataframes read from ZIP files"""
    # pass the provided directory argument.
    # use retrieveAllZIPs generator.
    geodataframes = []
    for zipfile in retrieveAllZIPs(directory):
        # for each ZIP read the shapefile and append the retruned geo dataframes
        # to a list of geodataframes
        geodataframes.append(readFromZIP(zipfile))
    return geodataframes