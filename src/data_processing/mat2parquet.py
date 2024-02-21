import numpy as np
import matplotlib.pyplot as plt
import polars as pl
import os
import scipy.io as sio
import pyarrow as pa
import pyarrow.parquet as pq

# Importing files from .mat-files and converting to polars dataframe
### Method 1: mat->dataframe ###
def fromMatToDf(file_path):
    mat = sio.loadmat(file_path)
    
    # Check if the main key 'Data' exists in the .mat file
    if 'Data' not in mat:
        return None

    main_data = mat['Data'][0][0]
    channels = main_data['Channel'][0]
    
    data_dict = {}
    for channel in channels:
        name = channel[0][0]
        data = channel[1].flatten()  # Flatten the numpy array
        data_dict[name] = data

    df = pl.DataFrame(data_dict)
    return df

def makeDataFrame(root_folder):
    dfs = []  # List to store individual DataFrames
    for month_folder in os.listdir(root_folder):
        month_path = os.path.join(root_folder, month_folder)
        if not os.path.isdir(month_path):
            continue
        for day_folder in os.listdir(month_path):
            day_path = os.path.join(month_path, day_folder)
            if not os.path.isdir(day_path):
                continue
            for file_name in os.listdir(day_path):
                if file_name.endswith(".mat"):
                    file_path = os.path.join(day_path, file_name)
                    df = fromMatToDf(file_path)
                    if df.shape[0] > 0:
                        pass # Placeholder. You can replace this with whatever processing you need.
                    if not df.is_empty():
                        dfs.append(df)
                        
    # Combine all DataFrames into one
    if dfs:
        final_df = pl.concat(dfs)
        return final_df
    return None

def makeDataFrameForOneDay(root_folder, target_month, target_day): # DataFrame
    dfs = []  # List to store individual DataFrames
    
    month_path = os.path.join(root_folder, target_month)
    if not os.path.isdir(month_path):
        return None
        
    day_path = os.path.join(month_path, target_day)
    if not os.path.isdir(day_path):
        return None
        
    for file_name in os.listdir(day_path):
        if file_name.endswith(".mat"):
            file_path = os.path.join(day_path, file_name)
            df = fromMatToDf(file_path)
            if df.shape[0] > 0:
                pass 
            if not df.is_empty():
                dfs.append(df)
                
    # Combine all DataFrames into one
    if dfs:
        final_df = pl.concat(dfs)
        return final_df
    return None

### Method 2: Save as Parquet ###
def fromMatToTable(file_path):
    mat = sio.loadmat(file_path)

    if 'Data' not in mat:
        return None
    
    main_data = mat['Data'][0][0]
    channels = main_data['Channel'][0]

    data_dict = {}
    for channel in channels:
        name = channel[0][0]
        data = channel[1].flatten()  # Flatten the numpy array
        data_dict[name] = data

    df = pl.DataFrame(data_dict)
    return df

def saveMatAsParquet(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    
    for month_folder in os.listdir(input_dir):
        month_path = os.path.join(input_dir, month_folder)
        if not os.path.isdir(month_path):
            continue

        # Create a new directory for each month within output_dir
        month_output_dir = os.path.join(output_dir, month_folder)
        os.makedirs(month_output_dir, exist_ok=True)

        for day_folder in os.listdir(month_path):
            day_path = os.path.join(month_path, day_folder)
            if not os.path.isdir(day_path):
                continue

            for file_name in os.listdir(day_path):
                if file_name.endswith(".mat"):
                    file_path = os.path.join(day_path, file_name)
                    table = fromMatToTable(file_path)
                    
                    if table is not None and not table.is_empty():
                        # Save as Parquet within the month's directory
                        parquet_file_name = os.path.splitext(file_name)[0] + ".parquet"
                        parquet_file_path = os.path.join(month_output_dir, parquet_file_name)
                        table.write_parquet(parquet_file_path)
                        
def combineParquetFiles(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True) 
    # Loop through the month-folders in input_dir
    for month_folder in os.listdir(input_dir):
        month_folder_path = os.path.join(input_dir, month_folder)
        # Check if the path is a directory before proceeding
        if os.path.isdir(month_folder_path):
            parquet_files = [os.path.join(month_folder_path, f) for f in os.listdir(month_folder_path) if f.endswith('.parquet')]
            # Combine the tables
            tables = [pq.read_table(f) for f in parquet_files]
            if tables:
                # Convert integer columns to double
                for table in tables:
                    for i, field in enumerate(table.schema):
                        if field.type == pa.int32():
                            tables[i] = table.set_column(i, field.name, table.column(i).cast(pa.float64()))
                combined_table = pa.concat_tables(tables)
                # Write to output
                pq.write_table(combined_table, os.path.join(output_dir, f"{month_folder}.parquet"))
