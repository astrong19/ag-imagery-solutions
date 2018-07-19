import rasterio
import numpy as np
from pprint import pprint

def describe_raster(sat_data):
    # Get the bounding box of this GeoTIFF
    bounds = sat_data.bounds

    #get pixel size
    w_meters = (sat_data.bounds.right - sat_data.bounds.left) / sat_data.width
    h_meters = (sat_data.bounds.top - sat_data.bounds.bottom) / sat_data.height

    #get coord system
    cs = sat_data.crs

    print("Bounding Box: {} \nPixel Width: {} \nPixel Height: {} \nCoordinate System: {}".format(bounds, w_meters, h_meters, cs))

def describe_bands(sat_data):

    array = sat_data.read()
    stats = []

    for band in array:
        stats.append({
        'min': band.min(),
        'mean': band.mean(),
        'median': np.median(band),
        'max': band.max()})

    pprint(stats)

if __name__ == '__main__':

    sat_data = rasterio.open(r'data\20180326_181856_103c_3B_AnalyticMS.tif')

    describe_bands(sat_data)
