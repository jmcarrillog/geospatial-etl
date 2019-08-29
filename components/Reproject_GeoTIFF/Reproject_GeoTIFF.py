import os
import sys

# this component requires gdalwrap to be installed in the host machine

def main():
    # input (GeoJSON file)
    in_file = sys.argv[1]
    # parameters (epsg codes)
    in_epsg = int(sys.argv[2])
    # parameters (epsg codes)
    out_epsg = int(sys.argv[3])
    # output (GeoTIFF file)
    out_file = sys.argv[4]
    # calling raster_reproject function
    reproject_raster(in_file, in_epsg, out_epsg, out_file)


def reproject_raster(in_file, in_epsg, out_epsg, out_file):
    # combining elements for the system call
    sys_call ="gdalwarp -s_srs EPSG:"+str(in_epsg)+" -t_srs EPSG:"+str(out_epsg)
    sys_call = sys_call+" -dstnodata -999999999.000000 -r bilinear -of GTiff "+in_file+" "+out_file
    os.system(sys_call)

main()
