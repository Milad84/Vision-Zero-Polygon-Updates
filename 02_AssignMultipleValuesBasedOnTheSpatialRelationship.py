import arcpy

# Set up layers
final_output_layer = "Final_Output_13"
zip_layer = "ZIPCodes_CopyFeatures"

# Create feature layers for spatial selection
arcpy.management.MakeFeatureLayer(final_output_layer, "final_layer")
arcpy.management.MakeFeatureLayer(zip_layer, "zip_layer")

# Create an update cursor to iterate over the polygons in Final_Output_13
with arcpy.da.UpdateCursor("final_layer", ["OID@", "SHAPE@", "zip_codes"]) as final_cursor:
    for final_row in final_cursor:
        final_polygon = final_row[1]  # Geometry of the polygon
        zip_codes = set()  # Using a set to store unique ZIP codes
        
        # Select zip code areas that intersect the current polygon
        arcpy.management.SelectLayerByLocation("zip_layer", "INTERSECT", final_polygon)
        
        # Create a search cursor to check the selected zip codes
        with arcpy.da.SearchCursor("zip_layer", ["ZIPCODE"]) as zip_cursor:
            for zip_row in zip_cursor:
                zip_code = str(zip_row[0])  # Convert ZIP code to string for storage
                zip_codes.add(zip_code)

        # Assign the concatenated values to zip_codes field, if any ZIP codes were found
        final_row[2] = ", ".join(sorted(zip_codes)) if zip_codes else None
        
        # Update the row
        final_cursor.updateRow(final_row)

# Clear the selection
arcpy.management.SelectLayerByAttribute("zip_layer", "CLEAR_SELECTION")
arcpy.management.SelectLayerByAttribute("final_layer", "CLEAR_SELECTION")
