import arcpy

# Set up layers
final_output_layer = "Final_Output_12"
engineering_layer = "Area_Engineering_CopyFeatures"

# Define council district mappings to directions
district_mapping = {
    1: "CENTRAL", 9: "CENTRAL",
    2: "SOUTH", 3: "SOUTH", 5: "SOUTH", 8: "SOUTH",
    4: "NORTH", 6: "NORTH", 7: "NORTH", 10: "NORTH"
}

# Add the field if it doesn't exist
if "area_eng_areas" not in [f.name for f in arcpy.ListFields(final_output_layer)]:
    arcpy.AddField_management(final_output_layer, "area_eng_areas", "TEXT")

# Make feature layers for spatial selection
arcpy.management.MakeFeatureLayer(final_output_layer, "final_layer")
arcpy.management.MakeFeatureLayer(engineering_layer, "engineering_layer")

# Create an update cursor to iterate over the polygons in Final_Output_12
with arcpy.da.UpdateCursor("final_layer", ["OID@", "SHAPE@", "area_eng_areas"]) as final_cursor:
    for final_row in final_cursor:
        final_oid = final_row[0]  # Get the OID for spatial selection
        final_polygon = final_row[1]  # Geometry of the polygon
        directions = set()  # Using a set to store unique directions
        
        # Select engineering areas that intersect the current polygon
        arcpy.management.SelectLayerByLocation("engineering_layer", "INTERSECT", final_polygon)

        # Create a search cursor to check the selected engineering areas
        with arcpy.da.SearchCursor("engineering_layer", ["SHAPE@", "COUNCIL_DISTRICT"]) as eng_cursor:
            for eng_row in eng_cursor:
                council_district = int(eng_row[1])  # Ensure council district is an integer
                if council_district in district_mapping:
                    directions.add(district_mapping[council_district])

        # Assign the concatenated values to area_eng_areas field, if any areas were found
        final_row[2] = ", ".join(sorted(directions)) if directions else None
        
        # Update the row
        final_cursor.updateRow(final_row)

# Clear the selection
arcpy.management.SelectLayerByAttribute("engineering_layer", "CLEAR_SELECTION")
arcpy.management.SelectLayerByAttribute("final_layer", "CLEAR_SELECTION")
