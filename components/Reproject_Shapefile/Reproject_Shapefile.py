import os
import sys
from osgeo import ogr, osr
from zipfile import ZipFile
from os.path import isfile, join


def main():
    # input (zip file)
    in_file = sys.argv[1]
    # parameters (epsg codes)
    in_epsg = int(sys.argv[2])
    out_epsg = int(sys.argv[3])
    # output (zip file)
    out_file = sys.argv[4]

    # prepare input shapefile name
    in_shapefile = in_file[:-4]+'.shp'
    # prepare output shapefile name
    out_shapefile = out_file[:-4]+'.shp'

    # unzip compressed file
    unzip_shapefile(in_file)

    # set driver
    driver = ogr.GetDriverByName('ESRI Shapefile')

    # call reproject function
    reproject_vector_file(in_shapefile, in_epsg, out_epsg, out_shapefile, driver)

    # zip the output shapefile
    zip_shapefile(out_file)

    # clean input and output folders from shapefile-related files other than zip files
    clean_folder(in_file)
    clean_folder(out_file)


def unzip_shapefile(in_file):
    with ZipFile(in_file, 'r') as zipObj:
        zipObj.extractall(os.path.dirname(in_file))


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


def reproject_vector_file(in_shapefile, in_epsg, out_epsg, out_shapefile, driver):

    # get the input layer
    inDataSet = driver.Open(in_shapefile)
    inLayer = inDataSet.GetLayer()

    # input SpatialReference
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(in_epsg)

    # output SpatialReference
    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(out_epsg)

    # create the CoordinateTransformation
    coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

    # create the output layer
    if os.path.exists(out_shapefile):
        driver.DeleteDataSource(out_shapefile)
    outDataSet = driver.CreateDataSource(out_shapefile)
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
        # reproject the geometry
        geom.Transform(coordTrans)
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

    # export .prj file
    outSpatialRef.MorphToESRI()
    prjfile = open(out_shapefile[:-4]+'.prj', 'w')
    prjfile.write(outSpatialRef.ExportToWkt())
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
