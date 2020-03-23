##########################
## Removes fields not required by TRANSLATED HABITAT DEF within ESRI Shapefiles or geodatabase featureclasses
## Enter folder (or geodatabase/dataset) containing the input shapefiles in the command prompt
## IMPORTANT: Ensure that the location entered contains ONLY SHAPEFILES TO BE EDITED.
##
## Created by: Graeme Duncan, JNCC for EMODnet Seabed Habitats 2014.
## Contact: info@emodnet-seabedhabitats.eu
###########################

import arcpy
import os

print "IMPORTANT: Ensure that the directory path entered below contains ONLY SHAPEFILES TO BE EDITED."
print "This script will remove fields from ALL SHAPEFILES within the supplied directory"
#set work space:
arcpy.env.overwriteOutput = True
root_workspace = raw_input('Paste the full directory path to the folder containing your habitat maps here: ')
arcpy.env.workspace = root_workspace
#define list of feature classes to work with:
fclist = arcpy.ListFeatureClasses()

add_fields = [
     ("GUI","TEXT",8),
     ("POLYGON","LONG","#"),
     ("ORIG_HAB","TEXT",255),
     ("HAB_TYPE","TEXT",20),
     ("ORIG_CLASS","TEXT",255),
     ("VERSION","TEXT",50),
     ("DET_MTHD","TEXT",255),
     ("DET_NAME","TEXT",255),
     ("DET_DATE","DATE","#"),
     ("TRAN_COM","TEXT",255),
     ("T_RELATE","TEXT",1),
     ("VAL_COMM","TEXT",255)]

errorCounter = 0

for fc in fclist:
    errorList = []
    field_name_list = [field.name for field in arcpy.ListFields(fc) if not (field.type in ["OID","Geometry"] or field.name.lower() in ["shape_length","shape_area"])]
    print fc
    for requiredField in add_fields:
        try:
            field_name_list.remove(requiredField[0])
        except ValueError as e:
            print "%s does not exist in featureclass %s" % (requiredField[0], fc)
            errorList.append(requiredField[0])
        #else:
            #print "Removing " + requiredField[0]
    if len(errorList) > 0:
        print "Could not find the following fields: %s" % errorList
        print "______________"
    print "Removing the following fields: "
    print field_name_list
    try:
        arcpy.DeleteField_management(fc,field_name_list)
    except Exception as e:
        print "error in removing fields from %s" % fc
        print e.message
        errorCounter += 1
    else:
        print "Fields deleted"
    finally:
        print "________________________________________________"
        print "________________________________________________"
print "There were %s errors" % str(int(errorCounter))
