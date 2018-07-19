# https://www.planet.com/docs/guides/quickstart-ndvi/
# https://en.wikipedia.org/wiki/Normalized_difference_water_index
import rasterio
import numpy as np
from xml.dom import minidom

def normalize(sat_data, xml_doc):
    #normalize the values in the arrays for each band using the Top of
    #Atmosphere (TOA) reflectance coefficients stored in metadata file

    # Load red and NIR bands - note all PlanetScope 4-band images have band order BGRN
    with rasterio.open(sat_data) as src:
        green = src.read(2)
        red = src.read(3)
        nir = src.read(4)

    print("Normalizing Raster")
    xmldoc = minidom.parse(xml_doc)
    nodes = xmldoc.getElementsByTagName("ps:bandSpecificMetadata")

    # XML parser refers to bands by numbers 1-4
    coeffs = {}
    for node in nodes:
        bn = node.getElementsByTagName("ps:bandNumber")[0].firstChild.data
        if bn in ['1', '2', '3', '4']:
            i = int(bn)
            value = node.getElementsByTagName("ps:reflectanceCoefficient")[0].firstChild.data
            coeffs[i] = float(value)

    # Multiply the Digital Number (DN) values in each band by the TOA reflectance coefficients
    band_green = green * coeffs[2]
    band_red = red * coeffs[3]
    band_nir = nir * coeffs[4]

    return src, band_green, band_red, band_nir

def calculate_ndvi(src, band_red, band_nir):

    print("calculating ndvi")
    # Allow division by zero
    np.seterr(divide='ignore', invalid='ignore')

    # Calculate NDVI
    ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

    save_image(src, ndvi, 'ndvi')

def calculate_ndwi(src, band_green, band_nir):
    # monitor changes related to water content in water bodies, using green and NIR wavelengths, defined by McFeeters (1996)

    print("calculating ndwi")
    # Allow division by zero
    np.seterr(divide='ignore', invalid='ignore')

    # Calculate NDVI
    ndwi = (band_green.astype(float) - band_nir.astype(float)) / (band_green + band_nir)

    save_image(src, ndwi, 'ndwi')

def save_image(src, image, index):

    # Set spatial characteristics of the output object to mirror the input
    print("saving image")
    kwargs = src.meta
    kwargs.update(
        dtype=rasterio.float32,
        count = 1)

    # Create the file
    if index == 'ndvi':
        output = r'data\ndvi.tif'
    elif index == 'ndwi':
        output = r'data\ndwi.tif'
    else:
        print("please specify valid index")

    with rasterio.open(output, 'w', **kwargs) as dst:
            dst.write_band(1, image.astype(rasterio.float32))

if __name__ == '__main__':

    #apecify path to imagery and metadata
    sat_data = r'data\20180326_181856_103c_3B_AnalyticMS.tif'
    xml_doc = r'data\20180326_181856_103c_3B_AnalyticMS_metadata.xml'

    #normalize and define red/nir bands
    src, band_green, band_red, band_nir = normalize(sat_data, xml_doc)

    #calculate ndvi and save
    calculate_ndwi(src, band_green, band_nir)
