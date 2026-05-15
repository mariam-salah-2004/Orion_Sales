import pandas as pd
import numpy as np

def transform_data(sales_df, forecast_df):

    forecast_df['ForecastDate'] = pd.to_datetime( forecast_df['Year'].astype(str) + '-01-01')  #date format
    forecast_df = forecast_df.drop_duplicates().reset_index(drop=True) # remove duplicates and reset index
#----------------------------------------------------------------
# remove duplicates and reset index
    sales_df = sales_df.drop_duplicates().reset_index(drop=True) 

# remove spaces from column names
    sales_df.columns = sales_df.columns.str.strip().str.replace(' ', '') 

# convert to string and title case
    sales_df['Name'] = sales_df['Name'].str.replace(',','')
    sales_df_columns=['Subcategory','Category','Name', 'Education', 'Occupation', 'ProductName', 'Brand','Color', 'Continent', 'State', 'City','CountryRegion']
    for col in sales_df_columns:                         
        sales_df[col] = sales_df[col].astype(str).str.title()

# extract last word from ProductName COLOR
    last_word = sales_df['ProductName'].str.split().str[-1] 
    sales_df['Color'] = last_word.apply(lambda x: x if (not str(x)[-1].isdigit()) else np.nan)
    sales_df['ProductName'] = sales_df.apply(
        lambda row: " ".join(row['ProductName'].split()[:-1]) if pd.notnull(row['Color']) else row['ProductName'], 
        axis=1
    )

# replace nulls
    sales_df['Color'] = sales_df['Color'].fillna('NA')
    sales_df['Name'] = sales_df['Name'].fillna('Unknown Customer')
    sales_df['Education'] = sales_df['Education'].fillna('Not Specified')
    sales_df['Occupation'] = sales_df['Occupation'].fillna('Not Specified')
    
# convert date columns to datetime
    sales_df['OrderDate'] = pd.to_datetime(sales_df['OrderDate'])
    forecast_df['ForecastDate'] = pd.to_datetime(forecast_df['ForecastDate'])

    sales_df['DateKey'] = sales_df['OrderDate'].dt.strftime('%Y%m%d').astype(int)
    forecast_df['DateKey'] = forecast_df['ForecastDate'].dt.strftime('%Y%m%d').astype(int)
    # 2. Creating Dimensions
    # Customer Dim
    customer_dim = sales_df[['CustomerKey', 'Name', 'Education', 'Occupation']].drop_duplicates().reset_index(drop=True)
    
    # Product Dim
    product_dim = sales_df[['ProductKey', 'ProductName']].drop_duplicates().reset_index(drop=True)
    
    # Category Dim
    category_dim = sales_df[['Subcategory', 'Category']].drop_duplicates().reset_index(drop=True)
    category_dim['CategoryKey'] = range(1, len(category_dim) + 1)
    
    # Color Junk Dim
    color_data = sales_df['Color'].drop_duplicates()
    color_junk_dim = pd.DataFrame(color_data, columns=['Color'])
    color_junk_dim['ColorKey'] = range(1, len(color_junk_dim) + 1)
    
    # Brand Dim (Role-playing)
    brand = pd.concat([sales_df['Brand'], forecast_df['Brand']]).drop_duplicates()
    brand_dim = pd.DataFrame({'Brand': brand})
    brand_dim['BrandKey'] = range(1, len(brand_dim) + 1)
    
    # Geo Dim
    geo_dim = sales_df[['Continent', 'State', 'City']].drop_duplicates().reset_index(drop=True)
    geo_dim['GeoKey'] = range(1, len(geo_dim) + 1)

    country = pd.concat([sales_df['CountryRegion'],forecast_df['CountryRegion']]).drop_duplicates().reset_index(drop=True)
    country_dim = pd.DataFrame({'CountryRegion': country})
    country_dim['CountryKey'] = range(1, len(country_dim) + 1)
    
    # Date Dim
    all_dates = pd.concat([sales_df['OrderDate'], forecast_df['ForecastDate']]).drop_duplicates()
    date_dim = pd.DataFrame({'FullDate': pd.to_datetime(all_dates)})

    date_dim['DateKey'] = date_dim['FullDate'].dt.strftime('%Y%m%d').astype(int)
    date_dim['Year'] = date_dim['FullDate'].dt.year
    date_dim['Month'] = date_dim['FullDate'].dt.month
    date_dim['Day'] = date_dim['FullDate'].dt.day

    # 3. Creating Fact Tables
    # Sales Fact
    sales_fact = sales_df.merge(category_dim, on=['Subcategory', 'Category'], how='left') \
                         .merge(color_junk_dim, on='Color', how='left') \
                         .merge(brand_dim, on='Brand', how='left') \
                         .merge(geo_dim, on=['Continent', 'State', 'City'], how='left') \
                         .merge(country_dim,on='CountryRegion',how='left')
    
    sales_fact = sales_fact[['DateKey', 'ProductKey', 'CustomerKey', 'CategoryKey', 'ColorKey', 'BrandKey', 'GeoKey', 'CountryKey', 'Quantity', 'NetPrice']]
    sales_fact.insert(0, 'SalesKey', range(1, len(sales_fact) + 1))
    
    # Forecast Fact
    forecast_fact = forecast_df.merge(country_dim,on='CountryRegion',how='left').\
        merge(brand_dim,on='Brand',how='left')

    
    forecast_fact = forecast_fact[['DateKey', 'CountryKey', 'BrandKey', 'Forecast']]
    forecast_fact.insert(0, 'ForecastKey', range(1, len(forecast_fact) + 1))

    # 4. Return All Tables
    return {
        'sales_fact': sales_fact,
        'forecast_fact': forecast_fact,
        'product_dim': product_dim,
        'customer_dim': customer_dim,
        'category_dim': category_dim,
        'color_dim': color_junk_dim,
        'brand_dim': brand_dim,
        'geo_dim': geo_dim,
        'date_dim': date_dim,
        'country_dim': country_dim
    }