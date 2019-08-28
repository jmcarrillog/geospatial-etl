from osgeo import ogr, osr
import os
import sys

def main():
    # inputs (filename)
    in_file = sys.argv[1]
    # parameters (epsg codes)
    in_epsg = int(sys.argv[2])
    out_epsg = int(sys.argv[3])
    # outputs (filename)
    out_file = sys.argv[4]

    # set driver
    driver = ogr.GetDriverByName('GeoJSON')

    # call reproject function
    reproject_vector_file(in_file, in_epsg, out_epsg, out_file, driver)

def reproject_vector_file(in_file, in_epsg, out_epsg, out_file, driver):

    # get the input layer
    inDataSet = driver.Open(in_file)
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
    if os.path.exists(out_file):
        driver.DeleteDataSource(out_file)
    outDataSet = driver.CreateDataSource(out_file)
    outLayer = outDataSet.CreateLayer(out_file, geom_type=inLayer.GetGeomType())

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

    # remove references to datasets
    inDataSet = None
    outDataSet = None

main()
