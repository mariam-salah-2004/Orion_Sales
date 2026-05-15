# Technical Assessment: Data Analytics Solutions Engineer (Orion Sales)
## Project Overview
This project demonstrates an end-to-end data engineering and analytics solution. It involves building a modular ETL pipeline using Python to transform unstructured JSON data into a structured Star Schema , followed by designing a high-performance Power BI dashboard to drive executive decision-making.

---
## 1. ETL Logic and Pipeline
The pipeline follows a modular architecture divided into three distinct phases:
### Phase 1: Extraction
* **Source**: Two JSON files containing historical sales transactions and forecasts.
* **Validation**: The script performs an initial quality check, identifying missing values notably in the Name, Education, and Occupation fields.
* **Observation**: The Sales dataset contained over 218,000 duplicate rows, which were addressed to ensure data integrity.
### Phase 2: Transformation
* **Data Cleansing**: Removed commas from customer names, stripped whitespace from column headers, and standardized text to Title Case.
* **Null Handling**: Filled missing values with descriptive placeholders.


* **Feature Engineering**:
* Parsed the last word of ProductName to populate the Color field.
* Converted date strings into integer-based DateKey formats (YYYYMMDD) for efficient joining.
* **Normalization**: Split the flat sales table into a Fact-and-Dimension structure.
### Phase 3: Loading
* **Export**: The final processed tables are exported as individual CSV files into a structured output folder.

## 2. Data Model (Star Schema)
The model is optimized to bridge the gap between sales transactions and yearly forecast targets.
### Fact Tables
* **sales_fact**: Transactional data linked to all dimensions.
* **forecast_fact**: Annual targets mapped at the Brand and Country level.
### Dimension Tables

| Table | Description |
| --- | --- |
| **product_dim** | Unique product registry.

| **customer_dim** | Demographic details with cleaned names.

| **category_dim** | Hierarchical grouping (Category/Subcategory).

| **geo_dim** | Granular data (Continent, State, City) used for Sales analysis.

| **country_dim** | Distinct from geo_dim to allow Forecast alignment at the country level.

| **brand_dim** | Conformed Dimension: Bridges Sales and Forecast for performance tracking.

| **color_dim** | Junk Dimension: Consolidates product colors into a single look-up table.

| **date_dim** | Role-Playing Dimension: Acts as a daily timeline for Sales and an annual anchor for Forecasts.

> **Note**: Data Model Visualization:
<img width="1776" height="772" alt="Screenshot 2026-05-16 001702" src="https://github.com/user-attachments/assets/a96f7d73-b805-40e2-a366-137f6e86ca0f" />
## 3. Key Modeling Decisions and Assumptions
* **Geography Granularity**: Separated country_dim from geo_dim because Forecasts only exist at the Country level, ensuring accurate alignment without duplicate rows.
* **Temporal Alignment**: Forecasts were normalized to January 1st of each year to enable the date_dim to bridge daily sales and annual targets.
* **Data Integrity**: Removing 218k+ exact duplicates was critical to prevent revenue overstatement and ensure a Single Source of Truth.
---
## 4. Analytical Insights and Dashboard Logic
The dashboard surfaces key KPIs and behavioral deep-dives:
* **Executive KPIs**: Total Sales ($42.64M) and a $3.55M Sales Difference between 2008 and 2009.
* **Actual vs. Forecast**: 2009 analysis shows approximately $9M in sales against a $39M target.
* **Regional Drivers**: The United States is identified as the core revenue driver at $34.33M.
* **Top 10 Products**: Bar charts pinpoint high-performers (e.g., Contoso Washer and Dryer) to guide inventory priorities.
* **Customer Behavior**: Drill-downs for clients (e.g., Zimmerman Henry at $1,776.29) track specific item preferences.

<img width="1487" height="812" alt="image" src="https://github.com/user-attachments/assets/d5717fbb-5d4c-40b8-852c-b97253a13264" />

## 5. Conclusion and Recommendations
By transforming unstructured data into a structured Star Schema, this solution shifts focus from basic reporting to Diagnostic Analytics.
**Key Strategic Recommendation**:
* While the US dominates revenue, Germany and China represent significant untapped potential.
* It is recommended that the marketing team launch targeted campaigns in these regions to diversify revenue streams.
