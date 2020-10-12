##########################
## Designed to work in Arcgis 10.1
## Creates Study Area polygons for all shapefiles within a chosen directory.
## Outputs Study Area features into a subfolder named "StudyAreas".
## Names shapefiles correctly.
## Collects GUI from original habitat map name and transfers across.
## Creates "SUM_CONF" field for values to be entered manually.
##
## Warning: The habitat maps contained within the supplied folder MUST be in a MESH DEF for this script to work.
## Created by: Graeme Duncan, JNCC for EMODnet Seabed Habitats 2014.
## Modified by: Sabrina Agnesi, ISPRA for EMODnet Seabed Habitats 2020.
## Contact: info@emodnet-seabedhabitats.eu
###########################
import arcpy
from arcpy import env
import os

env.overwriteOutput = True
print "Please ensure that all habitat maps are named correctly and in a MESH Data Exchange Format"
print ""
root_workspace = raw_input('Paste the full directory path to the folder containing your MESH formatted maps here and press enter: ')
arcpy.env.workspace = root_workspace
featureList = arcpy.ListFeatureClasses()

outdir = os.path.join(root_workspace, "StudyAreas")
if not os.path.isdir(outdir):
    try: 
        os.makedirs(outdir)
    except OSError:
        raise

for fc in featureList:
    print "Creating StudyArea for %s..." % fc
    fcName, fcExt = os.path.splitext(str(fc))
    fcGUI = fcName[:8]
    print fcGUI
    outfc = outdir + "\\" + fcGUI + "_StudyArea" + fcExt
    desc = arcpy.Describe(fc)
    spatref = desc.spatialReference
    extent = desc.extent
    pts = [arcpy.Point(extent.XMin, extent.YMin),
           arcpy.Point(extent.XMax, extent.YMin),
           arcpy.Point(extent.XMax, extent.YMax),
           arcpy.Point(extent.XMin, extent.YMax)]
    array = arcpy.Array(items=pts)
    poly = arcpy.Polygon(array, spatref)
    try:
        arcpy.CopyFeatures_management(poly, outfc)
    except Exception as e:
        print "Error creating StudyArea shapefile for %s" % fc
        print e.message
    else:
        print "Successfully created StudyArea shapefile for %s" % fc
        print outfc
    print "Creating DEF fields..."
    arcpy.AddField_management(outfc, "GUI", "TEXT", "", "",8)
    arcpy.AddField_management(outfc, "UUID", "TEXT", "","",36)
    arcpy.AddField_management(outfc, "AVAILABLE", "TEXT","","",13)
    arcpy.CalculateField_management(outfc, "GUI", '"' + fcGUI + '"', "PYTHON")
    arcpy.DeleteField_management(outfc,"Id")
    print "_______________________"
    
print "************"
print "* COMPLETE *"
print "************"
