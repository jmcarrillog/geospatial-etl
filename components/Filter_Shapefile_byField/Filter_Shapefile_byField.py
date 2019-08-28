import os
import sys
from osgeo import ogr, osr
from zipfile import ZipFile
from os.path import isfile, join


def main():
    # input (zip file)
    in_file = sys.argv[1]
    # 1st parameter (field)
    field = sys.argv[2]
    # 2nd parameter (field-value)
    field_value = sys.argv[3]
    # output (zip file)
    out_file = sys.argv[4]

    # prepare input shapefile name
    in_shapefile = in_file[:-4]+'.shp'
    # prepare output shapefile name
    out_shapefile = out_file[:-4]+'.shp'

    # unzip compressed file
    unzip_shapefile(in_file)

    # call field-filter function
    filter_by_field_value(in_shapefile, field, field_value, out_shapefile)

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


def filter_by_field_value(in_shapefile, field, field_value, out_shapefile):
    # prepare system call
    sys_call = "ogr2ogr -f \"ESRI Shapefile\" "+out_shapefile
    sys_call = sys_call+" -where \""+field+" = '"+field_value+"'\" "+in_shapefile
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
