import arcpy

# Define the paths for the old feature layer and the new output layer
old_feature_layer = r"G:\ATD\ACTIVE TRANS\Vision Zero\GIS\Polygon Update\Polygon Update\Default.gdb\Final_Output_4"
output_path = r"G:\ATD\ACTIVE TRANS\Vision Zero\GIS\Polygon Update\Polygon Update\Default.gdb"
output_name = "Final_Output_5"  # Output name for the new feature class

# Create a FieldMappings object
field_mappings = arcpy.FieldMappings()

# Step 1: Add fields from the old feature class that we want to retain, renaming them where necessary.
fields_to_keep = {
    'Location_ID': 'location_id',
    'description': 'location_name',
    'STREET_LEVEL': 'street_levels',         # Rename to match required order
    'IS_INTERSECTION': 'is_intersection',
    'IS_SVRD': 'is_service_road',
    'counci_district': 'council_districts'
}

# Loop through each field to keep, rename them, and add them to the FieldMappings object
for old_field_name, new_field_name in fields_to_keep.items():
    try:
        print(f"Processing field: {old_field_name}")
        field_map = arcpy.FieldMap()
        field_map.addInputField(old_feature_layer, old_field_name)
        
        # Rename the field in the output feature class
        output_field = field_map.outputField
        output_field.name = new_field_name
        output_field.aliasName = new_field_name
        field_map.outputField = output_field

        # Add this specific field to the field mappings
        field_mappings.addFieldMap(field_map)
    except Exception as e:
        print(f"Error processing field {old_field_name}: {e}")
        continue  # Skip the problematic field and move to the next one

# Step 2: Add new fields that are missing in the old feature class, in the exact order provided.
new_fields = [
    {'name': 'location_group', 'type': 'LONG'},               # location_group (integer)
    {'name': 'is_signalized', 'type': 'SHORT'},               # boolean (short integer)
    {'name': 'is_hin', 'type': 'SHORT'},                      # boolean (short integer)
    {'name': 'signal_eng_areas', 'type': 'TEXT', 'length': 50},
    {'name': 'area_eng_areas', 'type': 'TEXT', 'length': 50},
    {'name': 'zip_codes', 'type': 'TEXT', 'length': 10},
    {'name': 'apd_sectors', 'type': 'TEXT', 'length': 10},
    {'name': 'signal_id', 'type': 'LONG'},                   # integer
    {'name': 'created_by', 'type': 'TEXT', 'length': 50},
    {'name': 'created_at', 'type': 'DATE'},
    {'name': 'updated_by', 'type': 'TEXT', 'length': 50},
    {'name': 'updated_at', 'type': 'DATE'},
    {'name': 'geometry', 'type': 'POLYGON'}                  # geometry field
]

for new_field in new_fields:
    field_map = arcpy.FieldMap()
    
    # Create a new field definition
    new_field_def = arcpy.Field()
    new_field_def.name = new_field['name']
    new_field_def.aliasName = new_field['name']
    new_field_def.type = new_field['type']
    
    if 'length' in new_field:
        new_field_def.length = new_field['length']
    
    # Set the output field to the new field definition
    field_map.outputField = new_field_def
    field_mappings.addFieldMap(field_map)

# Step 3: Create the new feature class with the ordered fields and renamed fields
arcpy.FeatureClassToFeatureClass_conversion(old_feature_layer, output_path, output_name, field_mapping=field_mappings)

print(f"Feature layer '{output_name}' created with the specified fields in order.")
