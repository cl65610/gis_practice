import arcpy
import numpy
import pandas as pd

arcpy.env.workspace = r"C:\Users\Administrator\Documents\data"

mxd = arcpy.mapping.MapDocument('CURRENT')

mxd = arcpy.mapping.MapDocument('CURRENT')[0]
df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
newlayer = arcpy.mapping.Layer("C:\Users\Administrator\Documents\ArcGIS 10.4.1\Desktop\VNP14IMGTDL_NRT_Global_48h\VNP14IMGTDL_NRT_Global_48h.shp")
base = arcpy.mapping.Layer("C:\users\Administrator\Documents\ArcGIS\World Countries.lyr")
arcpy.mapping.AddLayer(df, newlayer)
arcpy.mapping.AddLayer(df, base)



# Initially, I thought that I was going to have to do some coordinate conversion in order to get the fire data to interact with
# Country border data, but that wasn't the case
# in_table = ("C:\Users\Administrator\Documents\ArcGIS 10.4.1\Desktop\VNP14IMGTDL_NRT_Global_48h\VNP14IMGTDL_NRT_Global_48h.shp")
# output_table = ("C:\Users\Administrator\Documents\ArcGIS 10.4.1\Desktop\VNP14IMGTDL_NRT_Global_48h\converted")
#arcpy.ConvertCoordinateNotation_management(input_table, output_table, "LONGITUDE", "LATITUDE", "DD_2", "DMS_1")


# Create a new layer that is the intersection of the country boundary layer and the fire data
arcpy.Intersect_analysis(["VNP14IMGTDL_NRT_Global_24h","World Countries"], "Joined")


#This was the first attempt I made at calculating those summary statistics. This was done
# before I realized that confifdence was a text-based categorical, and needed to be modified before this step.

arcpy.Statistics_analysis ("Intersected", "Summary_statistics", [["NAME", "COUNT"],["BRIGHT_TI5", "MAX"]], "NAME")
arr = arcpy.da.TableToNumPyArray("Summary_statistics", *)

# In order to get the highest confidence fire. I went this route
# This turns the intersected table into a numpy array. That array can then be converted to a dataframe
array = arcpy.da.TableToNumPyArray("Intersected", ["NAME", "CONFIDENCE", "BRIGHT_TI5", "LATITUDE", "LONGITUDE", "DAYNIGHT", "BRIGHT_TI4", "FID_VNP14I"])

intersect_df = pd.DataFrame(array)
df['confidence_numeric'] = df.CONFIDENCE.map({'low':1, 'nominal':2, 'high':3})

# Now that this column has been created, we can group by country
grouped = df.groupby("NAME")

# Aggregate the data fields that we're interested in
grouped_df = grouped.agg({'FID_VNP14I': numpy.count_nonzero, 'confidence_numeric': numpy.max, 'BRIGHT_TI5', numpy.max})

#Send this output to a csv
grouped_df.to_csv(r"C:\Users\Administrator\Documents\data\final_output", encoding = 'utf-8')
