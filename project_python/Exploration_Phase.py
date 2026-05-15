import pandas as pd
import json


import pandas as pd
import json

def extract_data(sales_path, forecast_path):
    print("--- Start Extraction Phase ---")
    
    data_sources = {
        'Forecast': forecast_path,
        'Sales': sales_path
    }
    
    dataframes = {}

    for name, path in data_sources.items():
        with open(path, 'r') as f:
            df = pd.DataFrame(json.load(f))
            dataframes[name] = df
        
        print(f"Rows loaded: {len(df)}")
        print(df.head()) 

        print(f"\nData Quality Issues in {name}:")
        print("Missing Values:\n", df.isnull().sum())
        print("\nData Types:\n", df.dtypes)

        print(f"\nDuplicate Values in {name} (per column):")
        for col in df.columns:
            dup_count = df[col].duplicated().sum()
            print(f"- {col}: {dup_count}")
        
        print(f"\nTotal Duplicate Rows in {name}: {df.duplicated().sum()}")

    sales_df = dataframes['Sales']
    forecast_df = dataframes['Forecast']

    unmapped_in_forecast = [col for col in forecast_df.columns if col not in sales_df.columns]
    print(f"\n--- Mapping Analysis ---")
    print(f"Unmapped in Forecast: {unmapped_in_forecast}")

    return sales_df, forecast_df

