import os
import sys
from osgeo import ogr, osr
from zipfile import ZipFile
from os.path import isfile, join


def main():
    # input GeoTIFF
    in_raster = sys.argv[1]
    # input Shapefile for clip boundary
    clip_boundary_file = sys.argv[2]
    # output GeoTIFF
    out_raster = sys.argv[3]

    # prepare input shapefile clip boundary name
    clip_boundary_shapefile = clip_boundary_file[:-4]+'.shp'

    # unzip compressed file
    unzip_shapefile(clip_boundary_file)

    # call raster clip function
    raster_clip(in_raster, clip_boundary_shapefile, out_raster)

    # clean input and output folders from shapefile-related files other than zip files
    clean_folder(clip_boundary_file)


def unzip_shapefile(in_file):
    with ZipFile(in_file, 'r') as zipObj:
        zipObj.extractall(os.path.dirname(in_file))


def raster_clip(in_raster, clip_boundary_shapefile, out_raster):
    # prepare system call
    sys_call = "gdalwarp -of GTiff -cutline "+clip_boundary_shapefile+" -crop_to_cutline -dstnodata -999999999.0 "
    sys_call = sys_call+in_raster+" "+out_raster
    os.system(sys_call)


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
