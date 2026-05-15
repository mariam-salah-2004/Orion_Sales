# Technical Assessment: Data Analytics Solutions Engineer (Orion Sales)

## Project Overview
This project demonstrates an end-to-end data engineering and analytics solution. It involves building a modular ETL pipeline using Python to transform unstructured JSON data into a structured Star Schema, followed by designing a high-performance Power BI dashboard to drive executive decision-making.

---

## 1. ETL Logic and Pipeline
[cite_start]The pipeline follows a modular architecture divided into three distinct phases[cite: 2]:

### Phase 1: Extraction
* [cite_start]Source: Two JSON files containing historical sales transactions and forecasts[cite: 3].
* [cite_start]Validation: Performed initial quality checks, identifying missing values in Name, Education, and Occupation fields[cite: 4].
* [cite_start]Observation: Identified over 218,000 duplicate rows in the Sales dataset, which were addressed to ensure data integrity[cite: 5].

### Phase 2: Transformation
* [cite_start]Data Cleansing: Removed commas from customer names, stripped whitespace from headers, and standardized text to Title Case[cite: 9, 11, 12].
* [cite_start]Null Handling: Filled missing values with descriptive placeholders[cite: 13].
* Feature Engineering: 
    * [cite_start]Parsed the last word of ProductName to populate a clean Color field[cite: 15].
    * [cite_start]Converted all date strings into integer-based DateKey (YYYYMMDD) for efficient modeling[cite: 16, 17].
* [cite_start]Normalization: Split the flat sales table into a Fact-and-Dimension structure[cite: 18].

### Phase 3: Loading
* [cite_start]Processed tables are exported as individual CSV files into a structured output folder[cite: 19].

---

## 2. Data Model (Star Schema)
[cite_start]The model is optimized to bridge the gap between sales transactions and yearly forecast targets[cite: 20, 21].

### Fact Tables
* [cite_start]sales_fact: Transactional data linked to all dimensions[cite: 23].
* [cite_start]forecast_fact: Annual targets mapped at the Brand and Country level[cite: 24].

### Dimension Tables
| Table | Description |
| :--- | :--- |
| product_dim | [cite_start]Unique product registry[cite: 26]. |
| customer_dim | [cite_start]Demographic details with cleaned names[cite: 26]. |
| category_dim | [cite_start]Hierarchical grouping (Category/Subcategory)[cite: 26]. |
| geo_dim | [cite_start]Granular data (Continent, State, City) used for Sales analysis[cite: 26]. |
| country_dim | [cite_start]Distinct from geo_dim to allow Forecast alignment at the country level[cite: 26, 29]. |
| brand_dim | [cite_start]Conformed Dimension: Bridges Sales and Forecast for performance tracking[cite: 26]. |
| color_dim | [cite_start]Junk Dimension: Consolidates product colors into a look-up table[cite: 26, 33]. |
| date_dim | [cite_start]Role-Playing Dimension: Acts as a daily timeline for Sales and an annual anchor for Forecasts[cite: 26, 30]. |

> **Note:** Data Model Visualization:
> ![Data Model](./data_model.png)

---

## 3. Key Modeling Decisions and Assumptions
* Geography Granularity: Separated country_dim from geo_dim because Forecasts only exist at the Country level. [cite_start]This prevents duplicate rows in regional visuals[cite: 29].
* [cite_start]Temporal Alignment: Forecasts were normalized to January 1st of each year to enable the date_dim to bridge daily sales and annual targets[cite: 30].
* [cite_start]Data Integrity: Removing 218k+ exact duplicates was critical to prevent revenue overstatement and ensure a Single Source of Truth[cite: 31, 32].

---

## 4. Analytical Insights and Dashboard Logic
[cite_start]The dashboard surfaces key KPIs and behavioral deep-dives[cite: 36]:

* [cite_start]Executive KPIs: Total Sales ($42.64M) with a $3.55M difference between 2008 and 2009[cite: 38].
* [cite_start]Actual vs. Forecast: 2009 analysis shows $9M in sales against a $39M target, highlighting a significant variance[cite: 39].
* [cite_start]Regional Drivers: The United States is the core revenue driver at $34.33M[cite: 41].
* [cite_start]Top 10 Products: High-performers like Contoso Washer and Dryer guide inventory priorities[cite: 43].
* [cite_start]Customer Behavior: Drill-downs (e.g., Zimmerman Henry at $1,776.29) track specific item preferences for targeted CRM[cite: 44].

---

## 5. Conclusion and Recommendations
[cite_start]By transforming unstructured data into a structured Star Schema, this solution shifts focus from basic reporting to Diagnostic Analytics[cite: 47, 48].

Key Strategic Recommendation:
* [cite_start]While the US dominates revenue, Germany and China represent significant untapped potential[cite: 50]. 
* [cite_start]It is recommended that the marketing team launch targeted campaigns in these regions to diversify revenue streams[cite: 51].

---

<img width="1776" height="772" alt="Screenshot 2026-05-16 001702" src="https://github.com/user-attachments/assets/a96f7d73-b805-40e2-a366-137f6e86ca0f" />
<img width="1487" height="812" alt="image" src="https://github.com/user-attachments/assets/d5717fbb-5d4c-40b8-852c-b97253a13264" />
