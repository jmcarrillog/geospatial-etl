import os
import sys
from osgeo import ogr, osr
from zipfile import ZipFile
from os.path import isfile, join


def main():
    # input (KML file)
    in_file = sys.argv[1]
    # parameters (epsg codes)
    in_epsg = int(sys.argv[2])
    # output (zip file)
    out_file = sys.argv[3]

    # prepare output shapefile name
    out_shapefile = out_file[:-4]+'.shp'

    # set driver for input file
    in_driver = ogr.GetDriverByName('KML')
    # set driver for output file
    out_driver = ogr.GetDriverByName('ESRI Shapefile')

    # call file conversion function
    convert_vector_file(in_file, in_epsg, out_shapefile, in_driver, out_driver)

    # zip the output shapefile
    zip_shapefile(out_file)

    # clean output folder from shapefile-related files other than zip file
    clean_folder(out_file)

def zip_shapefile(out_file):
    # determine output folder
    output_folder = os.path.dirname(out_file)
    # list all files in output folder
    all_files = [f for f in os.listdir(output_folder) if isfile(join(output_folder, f))]
    # create the zip file
    zip_file = ZipFile(out_file, 'w')
    # common name for all shapefile related output files
    common_name = os.path.basename(out_file)[:-4]
    # filter files corresponding to the output shapefile
    for item in all_files:
        if common_name in item:
            zip_file.write(join(output_folder, item), arcname=item)
    zip_file.close()


def convert_vector_file(in_file, in_epsg, out_shapefile, in_driver, out_driver):

    # get the input layer
    inDataSet = in_driver.Open(in_file)
    inLayer = inDataSet.GetLayer()

    # create the output layer
    if os.path.exists(out_shapefile):
        out_driver.DeleteDataSource(out_shapefile)
    outDataSet = out_driver.CreateDataSource(out_shapefile)
    outLayer = outDataSet.CreateLayer(out_shapefile[:-4], geom_type=inLayer.GetGeomType())

    # add fields
    inLayerDefn = inLayer.GetLayerDefn()
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        outLayer.CreateField(fieldDefn)

    # get the output layer's feature definition
    outLayerDefn = outLayer.GetLayerDefn()

    # loop through the input features
    inFeature = inLayer.GetNextFeature()
    while inFeature:
        # get the input geometry
        geom = inFeature.GetGeometryRef()
        # create a new feature
        outFeature = ogr.Feature(outLayerDefn)
        # set the geometry and attribute
        outFeature.SetGeometry(geom)
        for i in range(0, outLayerDefn.GetFieldCount()):
            outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))
        # add the feature
        outLayer.CreateFeature(outFeature)
        # dereference the features and get the next input feature
        outFeature = None
        inFeature = inLayer.GetNextFeature()

    # input SpatialReference
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(in_epsg)

    # export .prj file
    inSpatialRef.MorphToESRI()
    prjfile = open(out_shapefile[:-4]+'.prj', 'w')
    prjfile.write(inSpatialRef.ExportToWkt())
    prjfile.close()

    # remove references to datasets
    inDataSet = None
    outDataSet = None


# function that removes all shapefile related files other than the zip file
def clean_folder(zip_file):
    # determine folder
    folder = os.path.dirname(zip_file)
    # pattern
    remove_pattern = os.path.basename(zip_file)[:-4]
    # list all files in folder
    all_files = [f for f in os.listdir(folder) if isfile(join(folder, f))]
    # remove the files
    for item in all_files:
        if remove_pattern in item and '.zip' not in item:
            os.remove(join(folder, item))


main()
