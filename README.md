1. ETL Logic Overview
The pipeline follows a modular architecture divided into three distinct phases:
Phase 1: Extraction
•	Source: Two JSON files containing historical sales transactions  forecasts.
•	Validation: The script performs an initial quality check, identifying missing values (notably in the Name, Education, and Occupation fields of the Sales data) and high duplication rates.
•	Observation: The Sales dataset contained over 218,000 duplicate rows, which were addressed in the transformation phase to ensure data integrity.
Phase 2: Transformation
•	Data Cleansing:
o	String Formatting: Remove commas from customer names. 
o	Deduplication: Removed exact duplicates and stripped whitespace from column headers.
o	Standardization: Converted text fields to Title Case.
o	Null Handling: Filled missing values with descriptive placeholders 
•	Feature Engineering:
o	Color Extraction: Parsed the last word of ProductName to populate the Color field, ensuring the product name itself remains clean.
o	Date Keys: Converted all date strings into integer-based DateKey formats (YYYYMMDD) to facilitate efficient joining in the data model.
•	Normalization: Split the flat sales table into a Fact-and-Dimension structure.
Phase 3: Loading
•	The final processed tables are exported as individual CSV files into a structured output folder.
________________________________________
2. Data Model (Star Schema)
The model is optimized to bridge the gap between sales transactions and forecast targets.
Fact Tables
•	sales_fact: Transactional data linked to all dimensions.
•	forecast_fact: Annual targets mapped at the Brand and Country level.
Dimension Tables
Table	Description
product_dim	Unique product registry.
customer_dim	Demographic details with cleaned names.
category_dim	Hierarchical grouping (Category/Subcategory).
geo_dim	Granular data (Continent, State, City) used for Sales analysis.
country_dim	Kept distinct from geo_dim because the Forecast only provides "Country" data. This allows both Facts to join at the country level.
brand_dim	Confirmed Dimension: A shared attribute that bridges Sales and Forecast for performance tracking.
color_dim	Junk Dimension: Consolidates product colors into a single look-up table.
date_dim	Role-Playing Dimension: Acts as a daily timeline for Sales and an annual anchor for Forecasts .
________________________________________
. Key Modeling Decisions (Assumptions)
To resolve data discrepancies and optimize the model for high-performance DAX, the following strategic decisions were made:
•	Geography Granularity: We separated country_dim from the geo_dim . Since Forecasts only exist at the Country level, this separation ensures accurate alignment between Sales and Forecasts without duplicates rows in regional visuals.
•	Temporal Alignment: Forecasts were provided at a yearly grain. We normalized these to January 1st of each year to enable the date_dim to bridge daily sales and annual targets for "Actual vs. Forecast" time-series analysis.
•	Data Integrity: The Sales JSON contained 218k+ exact duplicates, which were treated as logging errors. Removing them was critical to prevent revenue overstatement and ensure a "Single Source of Truth."
•	Color Junk Dimension: A text-parsing heuristic was used to extract colors from the end of ProductName. This created a new analytical slice (Color Junk Dim) while reducing the storage footprint of the primary Product table.
4. Analytical Insights & Dashboard Logic
The model was engineered to drive executive decision-making through these key features:
•	Executive KPIs: Surfaced Total Sales ($42.64M) and a $3.55M Sales Diff between 2008 and 2009. 
•	Actual vs. Forecast: The 2009 analysis reveals a significant variance, with sales reaching ~$9M against a $39M target. This highlights the impact of our decision, allowing disparate data grains to coexist in one visual.
•	Regional & Product Mix: The donut chart identifies the United States ($34.33M) as the core revenue driver.
o	Top 10 Products: Bar charts pinpoint high-performers (e.g., Contoso Washer & Dryer), guiding inventory and procurement priorities.
•	Behavioral Deep-Dives: Drill-downs for clients like Zimmerman Henry ($1,776.29) track specific item preferences , enabling targeted CRM strategies.
o	Brand Funnel: The Top 5 Brands funnel (led by Contoso at 40K units) visualizes market demand and brand strength.
5. Conclusion & Recommendations
By transforming unstructured JSON into a structured Star Schema, this solution provides a Single Source of Truth. It shifts the focus from basic reporting to Diagnostic Analytics, enabling the team to pinpoint the exact drivers of business results.
Key Strategic Recommendation:
•	Market Expansion: The analysis shows that while the US dominates revenue, Germany and China represent significant untapped potential. It is recommended that the marketing team launch targeted campaigns in these regions to diversify the revenue stream and reduce dependency on a single market.

