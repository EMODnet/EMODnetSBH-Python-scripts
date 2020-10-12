##########################
## Adds correctly formatted ORIGINAL HABITAT DEF mandatory fields to ESRI Shapefiles or geodatabase featureclasses
## Enter folder (or geodatabase/dataset) containing the input shapefiles in the command prompt
## Script will check for mandatory fields and add if necessary.
## IMPORTANT: This script will NOT delete fields, this must be done manually once field data input is complete
##
## Created by: Graeme Duncan, JNCC for EMODnet Seabed Habitats 2014.
## Updated by ISPRA 2020-03-18: addition of COMP, COMP_TYPE and SUM_CONF field (MESH confidence assessment score)
## Contact: info@emodnet-seabedhabitats.eu
###########################

import arcpy
root_workspace = raw_input('Paste the full directory path to the folder containing your habitat maps here: ')
arcpy.env.workspace = root_workspace
newlist = arcpy.ListFeatureClasses()
#########

add_fields = [
     ("GUI","TEXT","#","#",8),
     ("POLYGON","LONG",8,"#","#"),
     ("ORIG_HAB","TEXT","#","#",254),
     ("ORIG_CLASS","TEXT","#","#",254),
     ("COMP","TEXT","#","#",10),
     ("COMP_TYPE","TEXT","#","#",20),
     ("SUM_CONF", "SHORT",5,"#","#")]

for fc in newlist:
## Add all fields
     print("Adding fields to " + str(fc) + " ...")
     field_name_list = [field.name for field in arcpy.ListFields(fc) if not (field.type in ["OID","Geometry"] or field.name in ["Shape_Length","Shape_Area"])]
     for fieldToAdd in add_fields:
         if fieldToAdd[0] not in field_name_list:
             print("Adding field " + str(fieldToAdd[0]) + " to " + str(fc) + " ")
             try:
                 arcpy.AddField_management(fc,fieldToAdd[0],fieldToAdd[1],fieldToAdd[2],fieldToAdd[3],fieldToAdd[4])
             except Exception as e:
                 print "Error ading field '%s' to %s" % (str(fieldToAdd[0]), str(fc))
                 print e.message
             else:
                 print "Field successfully added"
         else:
             print "Field '%s' already exists in %s, ignoring..." % (str(fieldToAdd[0]), str(fc))
     print "______________________"

raw_input('Process complete, press enter to quit')
