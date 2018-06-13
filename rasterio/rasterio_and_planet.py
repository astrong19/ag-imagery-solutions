import numpy as np
import rasterio

def describe_raster(sat_data):
    # Get the bounding box of this GeoTIFF
    bounds = sat_data.bounds

    #get pixel size
    w_meters = (sat_data.bounds.right - sat_data.bounds.left) / sat_data.width
    h_meters = (sat_data.bounds.top - sat_data.bounds.bottom) / sat_data.height

    print("Bounding Box: {} \nPixel Width: {} \nPixel Height: {} ".format(bounds, w_meters, h_meters))

if __name__ == '__main__':

    sat_data = rasterio.open(r'data\20180326_181856_103c_3B_AnalyticMS.tif')

    describe_raster(sat_data)
