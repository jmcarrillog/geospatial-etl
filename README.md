# Extract Transform Load (ETL) Python tools for Geospatial data

This repository includes multiple tools to perform Extract-Transform-Load (ETL) operations on Geospatial data, implemented as components for the WINGS semantic workflow system. WINGS is a system that helps scientists design and run experiments represented as workflows, for more information visit the [WINGS](www.wings-workflows.org) website.

The tools are implemented as Python scripts that can also be used from the command line in Linux systems. Internally, the Python scripts are calling [GDAL](https://gdal.org/) tools. Each script has particular inputs and outputs, and in some cases also parameters to configure the data processing operation.


## Application example: Preparing a Digital Elevation Model

Scientific models in Geosciences use spatial datasets such as Shapefiles and Digital Elevation Models DEMs as inputs; however, most of these datasets need to be prepared before they can be feed into the models. Therefore, tools to perform Extract-Transform-Load (ETL) operations over Geospatial data are fundamental for the completion of most experiments. Figure 1 shows the common usage of models in Geosciences.

![Figure 1](/figures/geosciences-models-usage.png)
Figure 1. Common usage of models in Geosciences.

As an example, we use some of the ETL tools in this repository to prepare a DEM for further analysis in hydrological models. The data preparation processing includes merging two raster tiles, reprojecting the result to a local reference system and then clipping it to a specific area of interest defined by a polygon in a Shapefile. Figure 2 illustrates the merging and clipping of two DEM tiles in the region of Aweil Centre in South Sudan.

![Figure 2](/figures/dem-before-after.png)
Figure 2. DEM tiles before and after the data preparation workflow.

These tools are combined to form a complete workflow in the WINGS system as shown in Figure 3. Light blue boxes at the top represent raw datasets, green boxes are parameters such as the coordinate reference system to use, yellow boxes are processing components and dark blue boxes are output datasets.

![Figure 3](/figures/etl-workflow.png)
Figure 3. Workflow for DEM preparation in WINGS.

The resulting DEM is ready for use in multiple Geosciences models as well as conventional GIS Software such as [QGIS](https://qgis.org/).

---

## Description of software components

Below you will find brief descriptions of each component, including its inputs, parameters, and outputs.


#### [Clip_GeoTIFF](/components/Clip_GeoTIFF)

Receives a GeoTIFF raster file and clips it using a vector clip file.

**Inputs**
* A raster file in GeoTIFF format.
* A vector file in shapefile format.

**Parameters**
* None

**Outputs**
* A raster file in GeoTIFF format.


#### [Filter_Shapefile_byField](/components/Filter_Shapefile_byField)

Receives a shapefile vector file and returns a shapefile vector file filtered with the elements that correspond to certain field-value pair.
  
  **Inputs**
  * A vector file in shapefile format.
  
  **Parameters**
  * Field name.
  * Field value.
  
  **Outputs**
  * A filtered vector file in shapefile format.


#### [GeoJSON_to_Shapefile](/components/GeoJSON_to_Shapefile)

Converts a GeoJSON file into a shapefile.

**Inputs**
* A vector file in GeoJSON format.

**Parameters**
* EPSG code of the input GeoJSON as defined in the [EPSG](http://www.epsg.org/) collection.

**Outputs**
* A vector file in shapefile format.


#### [KML_to_Shapefile](/components/KML_to_Shapefile)

Converts a KML file into a shapefile.

**Inputs**
* A vector file in KML format.

**Parameters**
* EPSG code of the input KML as defined in the [EPSG](http://www.epsg.org/) collection.

**Outputs**
* A vector file in shapefile format.


#### [Merge_raster](/components/Merge_raster)

Merges two raster files in GeoTIFF format into one.

**Inputs**
* Two raster files in GeoTIFF format.

**Parameters**
* None

**Outputs**
* A raster file in GeoTIFF format.


#### [Reproject_GeoJSON](/components/Reproject_GeoJSON)

Reprojects a GeoJSON file to another coordinate reference system. GeoJSON files are expected to use geographic coordinates in datum WGS 84. See [GeoJSON](https://tools.ietf.org/html/rfc7946) file format reference.

**Inputs**
* A vector file in GeoJSON format.

**Parameters**
* EPSG code of the input GeoJSON as defined in the [EPSG](http://www.epsg.org/) collection.
* EPSG code of the output GeoJSON as defined in the [EPSG](http://www.epsg.org/) collection.

**Outputs**
* A vector file in GeoJSON format.


#### [Reproject_GeoTIFF](/components/Reproject_GeoTIFF)

Reprojects a GeoTIFF file to another coordinate reference system.

**Inputs**
* A raster file in GeoTIFF format.

**Parameters**
* EPSG code of the input GeoTIFF as defined in the [EPSG](http://www.epsg.org/) collection.
* EPSG code of the output GeoTIFF as defined in the [EPSG](http://www.epsg.org/) collection.

**Outputs**
* A raster file in GeoTIFF format.


#### [Reproject_Shapefile](/components/Reproject_Shapefile)

Reprojects a shapefile file to another coordinate reference system.

**Inputs**
* A vector file in shapefile format.

**Parameters**
* EPSG code of the input shapefile as defined in the [EPSG](http://www.epsg.org/) collection.
* EPSG code of the output shapefile as defined in the [EPSG](http://www.epsg.org/) collection.

**Outputs:**
* A vector file in shapefile format.

---

### Acknowledgements

Juan Carrillo was financially supported for this project by the [Mitacs Globalink Research Award](https://www.mitacs.ca/en/programs/globalink) and the University of [Waterloo Machine Learning Lab](https://uwaterloo.ca/scholar/mcrowley/lab). Juan Carrillo gives special thanks to Mark Crowley, Daniel Garijo, and Yolanda Gil for their mentoring and contributions during this research project. Last but not least thanks to the administrative staff at Mitacs and the [Information Sciences Institute](https://www.isi.edu/) at University of Southern California for their kind help with multiple requirements.
