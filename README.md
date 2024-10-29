# Vision Zero Polygon Update Project

This repository contains scripts and documentation for managing and updating GIS polygon data for the Vision Zero initiative. The project includes data transformation, field mapping, and conditional spatial join to ensure accurate and standardized data for traffic safety analysis. These tools, designed for ArcGIS Pro, support complex spatial relationships and consolidate intersecting attributes into a single, usable dataset.
![image](https://github.com/user-attachments/assets/96dc6b52-eb1e-4c0d-bcba-330f153fabc0)

## Project Overview

The Vision Zero Polygon Update Project addresses the following goals:

- **Standardize and update** GIS polygon data for the Vision Zero dataset integration.
- **Assign accurate attribute data** (e.g., ZIP codes, council districts, engineering areas) to polygons based on spatial relationships.
- **Enable efficient data processing** with ArcPy and automate updates to maintain data accuracy and consistency.

## Features

- **Field Mapping and Standardization**: Automate field mapping across layers to ensure all data adheres to a consistent schema.
- **Handling One-to-Many Relationships**: Consolidate multiple intersecting attributes (ZIP codes, council districts, engineering areas) into single fields, using sets to avoid duplication.
- **Incremental Data Updates**: Track transformations by saving intermediate outputs for easy comparison and reproducibility.
- **Attribute Assignment**: Use spatial joins to assign directional data, intersection status, and other attributes based on polygon intersections.



