import os


def load_data(processed_tables, output_folder='output_data'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    for name, df in processed_tables.items():
        file_path = os.path.join(output_folder, f"{name}.csv")
        df.to_csv(file_path, index=False)