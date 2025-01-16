##########################
## Designed to work in Arcgis 10.1
## Creates Study Area polygons for all shapefiles within a chosen directory.
## See https://emodnet.ec.europa.eu/sites/emodnet.ec.europa.eu/files/public/Data%20Preparation%20Guide%20for%20Point%20Datasets%20v1_2.pdf for written guidance on the data schema
## Outputs Study Area features into a subfolder named "StudyAreas".
## Names shapefiles correctly.
## Collects GUI from original habitat map name and transfers across.
## Creates "SUM_CONF" field for values to be entered manually.
##
## Warning: The habitat maps contained within the supplied folder MUST be in a MESH DEF for this script to work.
## Created by: Graeme Duncan, JNCC for EMODnet Seabed Habitats 2014.
## Updated by JNCC 2019-12-19: removal of SUM_CONF field (it's been moved to the translated habitat DEF)
## Contact: helpdesk@emodnet.ec.europa.eu
###########################
import arcpy
from arcpy import env
import os

env.overwriteOutput = True
print "Please ensure that all habitat maps are named correctly and in a MESH Data Exchange Format"
print ""
root_workspace = raw_input('Paste the full directory path to the folder containing your MESH formatted maps here and press enter: ')
env.workspace = root_workspace
featureList = arcpy.ListFeatureClasses()

for fc in featureList:
    print "Creating StudyArea for %s..." % fc
    print "Creating DEF fields..."
    arcpy.AddField_management(fc, "GUI","TEXT","#","#",8)
    arcpy.AddField_management(fc, "UUID", "TEXT","#","#", 36)
    arcpy.AddField_management(fc, "AVAILABLE", "TEXT","#","#", 13)
    print "_______________________"
    
print "************"
print "* COMPLETE *"
print "************"
