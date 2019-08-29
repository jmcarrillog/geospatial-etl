# Extract Transform Load tools for Spatial data in WINGS

This repository includes multiple tools to perform Extract-Transform-Load (ETL) operations on Geospatial data, implemented as components for the WINGS semantic workflow system. WINGS is a system that helps scientists design and run experiments represented as workflows, for more information visit the [WINGS](www.wings-workflows.org) website.

The tools are implemented as Python scripts that be used from the command line in Linux systems. Internally, the Python scripts are calling [GDAL](https://gdal.org/) tools. Each script has particular inputs and outputs, and in some cases also parameters to configure the data processing operation.


## Application example: Preparing a Digital Elevation Model

Scientific models in Geosciences use spatial datasets such as Shapefiles and Digital Elevation Models DEMs as inputs; however, most of these datasets need to be prepared before they can be feed into the models. Therefore, tools to perform Extract-Transform-Load (ETL) operations over Geospatial data are fundamental for the completion of most experiments. Figure 1 shows the common usage of models in Geosciences.

Insert Fig. 1

As an example, we use some of the ETL tools in this repository to prepare a DEM for further analysis in hydrological models. The data preparation processing includes merging two raster tiles, reprojecting the result to a local reference system and then clipping it to a specific area of interest represented by a shapefile. These tools are combined to form a complete workflow in the WINGS system as shown in Figure 2.

Insert Fig. 2

Figure 3 illustrates the processing steps for two tiles of a DEM in the region of Aweil Centre in South Sudan.

Insert Fig. 3

The resulting DEM is ready for use in multiple Geosciences models.

## Tools description

---

### Clip_GeoTIFF

  **Description** Receives a GeoTIFF raster file and clips it using a vector clip file.
  
  **Inputs**
    
  * A raster file in GeoTIFF format.
  * A vector file in shapefile format.
  
  **Parameters**
    
  * None
  
  **Outputs:**
    
  * A raster file in GeoTIFF format.
  
---

### Filter_Shapefile_byField

  **Description** Receives a shapefile vector file and returns a shapefile vector file filtered with the elements that correspond to certain field-value pair.
  
  **Inputs**
    
  * A vector file in shapefile format.
  
  **Parameters**
    
  * Field name.
  * Field value.
  
  **Outputs:**
    
  * A filtered vector file in shapefile format.

---

### GeoJSON_to_Shapefile

  **Description** Converts a GeoJSON file into a shapefile.
  
  **Inputs**
    
  * A vector file in GeoJSON format.
  
  **Parameters**
    
  * EPSG code of the input GeoJSON as defined in the [EPSG](http://www.epsg.org/) collection.
  
  **Outputs:**
    
  * A vector file in shapefile format.
  
---

### KML_to_Shapefile

  **Description** Converts a KML file into a shapefile.
  
  **Inputs**
    
  * A vector file in KML format.
  
  **Parameters**
    
  * EPSG code of the input KML as defined in the [EPSG](http://www.epsg.org/) collection.
  
  **Outputs:**
    
  * A vector file in shapefile format.

---

### Merge_raster

  **Description** Merges two raster files in GeoTIFF format into one.
  
  **Inputs**
    
  * Two raster files in GeoTIFF format.
  
  **Parameters**
    
  * None
  
  **Outputs:**
    
  * A raster file in GeoTIFF format.
  
---

### Reproject_GeoJSON

  **Description** Reprojects a GeoJSON file to another coordinate reference system. GeoJSON files are expected to use geographic coordinates in datum WGS 84. See [GeoJSON](https://tools.ietf.org/html/rfc7946) file format reference.
  
  **Inputs**
    
  * A vector file in GeoJSON format.
  
  **Parameters**
    
  * EPSG code of the input GeoJSON as defined in the [EPSG](http://www.epsg.org/) collection.
  * EPSG code of the output GeoJSON as defined in the [EPSG](http://www.epsg.org/) collection.
  
  **Outputs:**
    
  * A vector file in GeoJSON format.
  
---

### Reproject_GeoTIFF

  **Description** Reprojects a GeoTIFF file to another coordinate reference system.
  
  **Inputs**
    
  * A raster file in GeoTIFF format.
  
  **Parameters**
    
  * EPSG code of the input GeoTIFF as defined in the [EPSG](http://www.epsg.org/) collection.
  * EPSG code of the output GeoTIFF as defined in the [EPSG](http://www.epsg.org/) collection.
  
  **Outputs:**
    
  * A raster file in GeoTIFF format.
  
---

### Reproject_Shapefile

  **Description** Reprojects a shapefile file to another coordinate reference system.
  
  **Inputs**
    
  * A vector file in shapefile format.
  
  **Parameters**
    
  * EPSG code of the input shapefile as defined in the [EPSG](http://www.epsg.org/) collection.
  * EPSG code of the output shapefile as defined in the [EPSG](http://www.epsg.org/) collection.
  
  **Outputs:**
    
  * A vector file in shapefile format.
  
---
