import os
import sys

# this component requires gdalwrap to be installed in the host machine

def main():
    # input (1st GeoTIFF file)
    in_file_1 = sys.argv[1]
    # input (2nd GeoTIFF file)
    in_file_2 = sys.argv[2]
    # output (GeoTIFF file)
    out_file = sys.argv[3]
    # calling merge_raster function
    merge_raster(in_file_1, in_file_2, out_file)


def merge_raster(in_file_1, in_file_2, out_file):
    # combining elements for the system call
    sys_call = "gdal_merge.py -ot Int16 -of GTiff -o "+out_file+" "+in_file_1+" "+in_file_2
    os.system(sys_call)

main()
