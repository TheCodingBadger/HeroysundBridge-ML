import os
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq
from datetime import datetime
from pathlib import Path

def days_since_start(filename):
    year = int(filename[0:4])
    month = int(filename[4:6])
    day = int(filename[6:8])
    
    date = datetime(year, month, day)
    start_date = datetime(2019, 12, 31)
    
    days_difference = (date - start_date).days
    return days_difference

def hours_since_start(filename):
    year = int(filename[0:4])
    month = int(filename[4:6])
    day = int(filename[6:8])
    hour = int(filename[8:10])
    
    date = datetime(year, month, day, hour)
    start_date = datetime(2019, 12, 31)
    
    hours_difference = (date - start_date).total_seconds() / 3600  # Convert seconds to hours
    return hours_difference

def add_columns(parquet_file_path, output_file_path, time_difference_function):
    dataset = ds.dataset(parquet_file_path, format="parquet")
    table = dataset.to_table()
    filename = os.path.basename(parquet_file_path)
    basename, _ = os.path.splitext(filename)
    time_difference = time_difference_function(basename)
    num_rows = len(table)
    
    # Create new columns as Arrow Arrays
    time_column = pa.array([int(time_difference)] * num_rows, type=pa.int64())  # Using int64 for hours
    filename_column = pa.array([basename] * num_rows, type=pa.string())
    
    # Get existing columns
    existing_columns = {name: table.column(name) for name in table.schema.names}
    
    # Combine new columns with the existing columns
    all_columns = {'Time_since_2019.12.31': time_column, 'Date': filename_column, **existing_columns}
    
    # Create a new table
    new_table = pa.table(all_columns)
    
    # Write the new table to a Parquet file
    pq.write_table(new_table, str(output_file_path))

def adding_date_filename_parquet(input_directory, output_directory):
    input_dir_path = Path(input_directory)
    output_dir_path = Path(output_directory)
    
    for year_dir in input_dir_path.iterdir():
        if year_dir.is_dir():
            for month_dir in year_dir.iterdir():
                if month_dir.is_dir():
                    for parquet_file in month_dir.glob('*.parquet'):
                        # Extract year, month, and day from the filename
                        filename = parquet_file.name
                        year, month, day = filename[:4], filename[4:6], filename[6:8]
                        
                        # Create the corresponding month and day subdirectories in the output directory
                        output_year_dir = output_dir_path / f'date_year={year}'
                        output_month_dir = output_year_dir / f'date_month={month}'
                        output_day_dir = output_month_dir / f'date_day={day}'
                        output_day_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Construct the input and output file paths
                        input_file_path = parquet_file
                        output_file_path = output_day_dir / filename
                        
                        # Process the file
                        add_columns(input_file_path, output_file_path, hours_since_start)


#input_directory = r'D:\Raw parquet'
#output_directory = r'D:\14.11.2023'
#adding_date_filename_parquet(input_directory, output_directory)
# file = r'D:\14.11.2023\date_year=2022\date_month=02\date_day=02\20220202002339.parquet'
# table = pq.read_table(file).to_pandas()
# print(table)
# file = r'D:\14.11.2023\date_year=2022\date_month=02\date_day=02\20220202012340.parquet'
# table = pq.read_table(file).to_pandas()
# print(table)
#file = r'D:\aggregated_data.parquet'
#table = pq.read_table(file).to_pandas()
#print(table)