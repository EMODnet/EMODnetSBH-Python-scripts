##########################
## EMODnet Seabed Habitats Data Exchange Format (DEF) for Maps of Seabed Habitats and Coastal Wetlands (v2022)
##
## This script adds the fields described in the EMODnet Seabed Habitats Data Exchange Format (DEF) for maps of
## seabed habitats and coastal wetlands v2022 (see emodnet-seabedhabitats.eu/contribute-data/data-exchange-format)
## to a set of ESRI Shapefiles or geodatabase feature classes.
## Enter folder (or geodatabase/dataset) containing the input Shapefiles/feature classes in the command prompt
## Script will check for the existence of the DEF fields and add if necessary.
## IMPORTANT:
##   - This script will NOT delete fields, this must be done manually once field data input is complete
##   - If a field already exists, you need to check that its format and length match the requirements of the DEF
##
## Created by: Graeme Duncan, JNCC for EMODnet Seabed Habitats 2014.
## Updated by JNCC 2019-12-19: addition of SUM_CONF field (MESH confidence assessment score)
## Updated by ISPRA 2020-03-18: addition of COMP and COMP_TYPE fields 
## Updated by JNCC 2022-07-25: consolidation of multiple DEFs into a single multi-purpose DEF
## Contact: emodnet-seabedhabitats.eu/helpdesk/contact-us/
###########################

import arcpy
root_workspace = raw_input('Paste the full directory path to the folder containing your habitat maps here: ')
arcpy.env.workspace = root_workspace
newlist = arcpy.ListFeatureClasses()
#########

add_fields = [
     ("GUI","TEXT","#","#",8),
     ("POLYGON","TEXT","#","#",10),
     ("ORIG_HAB","TEXT","#","#",254),
     ("ORIG_CLASS","TEXT","#","#",150),
     ("HAB_TYPE","TEXT","#","#",100),
     ("HAB_CLASS","TEXT","#","#",150), # Previously called 'VERSION' in Translated Habitat DEF
     ("DET_MTHD","TEXT","#","#",254),
     ("DET_NAME","TEXT","#","#",254),
     ("DET_DATE","DATE","#","#","#"),
     ("TRAN_COM","TEXT","#","#",254),
     ("T_RELATE","TEXT","#","#",1),
     ("VAL_COMM","TEXT","#","#",254),
     ("COMP","TEXT","#","#",10),
     ("COMP_TYPE","TEXT","#","#",20),
     ("SUM_CONF", "SHORT",5,"#","#"),
     ("TEXT_CONF","TEXT","#","#",100)]

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
