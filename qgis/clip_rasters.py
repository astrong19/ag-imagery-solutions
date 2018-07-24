import glob
import os
from qgis.core import *

def run_script(iface):
    '''needed for qgis scriptrunner plugin'''
    raster_path = os.getcwd()
    get_rasters(raster_path)

def get_rasters(raster_path):
    '''get rasters from file location'''
    print("Finding rasters in {}".format(raster_path))
    rasters = []

    for folder in os.listdir(raster_path):
        raster = glob.glob(r'{}/{}/*.tif'.format(raster_path, folder))
        rasters.append(raster)

    raster_list = [item for sublist in rasters for item in sublist]

    print(raster_list)
