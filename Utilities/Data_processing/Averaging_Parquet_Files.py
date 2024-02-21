import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path
import pyarrow as pa
import pyarrow.dataset as ds
import polars as pl
import numpy as np
import os




def check_value(value):
    # Check if the value is an integer, if so, return 0.0, else return the value itself
    if isinstance(value, int):
        return 0.0
    return value

def process_file(parquet_file):
    # Create a dataset
    dataset = ds.dataset(parquet_file, format="parquet")
    
    # Convert to polars DataFrame
    df = dataset.to_table().to_pandas()
    df = pl.DataFrame(df)
    
    # Get the total number of rows in the DataFrame
    total_rows = df.shape[0]
    
    # Calculate the size of each group
    group_size = total_rows // 1  # This will floor divide to get 60 groups
    
    # Create a new column for group numbers
    index_column = pl.DataFrame({
        'index': np.arange(total_rows)  # Create an array from 0 to total_rows-1
    })
    df = df.hstack(index_column)  # Add the index column to df
    group_numbers = (pl.col('index') // group_size).alias('group_num')
    
    # Add the group number column to the DataFrame
    df = df.with_columns(group_numbers)

    # Check if the 'Omega_N' column exists
    if 'Omega_N' in [col.name for col in df.get_columns()]:
        # If it exists, apply the check_value function to correct it
        corrected_omega_n_column = pl.col('Omega_N').map_elements(check_value, return_dtype=pl.Float64).alias('Omega_N')
        df = df.with_columns(corrected_omega_n_column)
    else:
        # If it doesn't exist, create it with all zeros
        total_rows = df.shape[0]  # Get the total number of rows in the DataFrame
        zeros = [0.0] * total_rows  # Create a list of zeros
        omega_n_column = pl.DataFrame({'Omega_N': zeros})  # Create a new DataFrame with the zeros
        df = df.hstack(omega_n_column)  # Add the new column to df

    # Check and handle integer values in 'Omega_N' column
    corrected_omega_n_column = pl.col('Omega_N').map_elements(check_value, return_dtype=pl.Float64).alias('Omega_N')
    df = df.with_columns(corrected_omega_n_column)

    
    
    # Now, group by the 'group_num' column and compute the mean for each group.
    # The first two columns will be identical for each group, so we'll take the first value of these columns in each group.
    aggregated_df = (
        df.group_by('group_num')
        .agg(
            pl.col('Time_since_2019.12.31').first().alias('Days_since_2019.12.31'),
            pl.col('Date').first().alias('Date'),
            pl.col('Point_1_N').mean().alias('Point_1_N_mean'),
            pl.col('Point_2_N').mean().alias('Point_2_N_mean'),
            pl.col('Point_3_N').mean().alias('Point_3_N_mean'),
            pl.col('Point_4_S').mean().alias('Point_4_S_mean'),
            pl.col('Point_5_S').mean().alias('Point_5_S_mean'),
            pl.col('Point_6_S').mean().alias('Point_6_S_mean'),
            pl.col('Omega_N').mean().alias('Omega_N_mean'),
            pl.col('Omega_S').mean().alias('Omega_S_mean'),
            pl.col('PT100_Temperature').mean().alias('PT100_Temperature_mean'),
        )
    )
    sorted_df = aggregated_df.sort('group_num')
    

    return sorted_df


#spesific_path = r'C:\Users\200408\OneDrive - Betonmast\Skrivebord\NTNU\Prosjektoppgave\Test\date_year=2022\date_month=05\date_day=05\20220505023134.parquet'
#print(process_file(spesific_path))

def averaging_parquetfiles(input_directory, output_file_path):
    input_dir_path = Path(input_directory)
    aggregated_data = None

    for year_dir in input_dir_path.iterdir():
        if year_dir.is_dir():
            print(year_dir)
            for month_dir in year_dir.iterdir():
                print(month_dir)
                if month_dir.is_dir():
                    for day_dir in month_dir.iterdir():
                        if day_dir.is_dir():
                            for parquet_file in day_dir.glob('*.parquet'):
                                file_data = process_file(parquet_file)
                                # Convert Polars DataFrame to Pandas DataFrame
                                file_data = file_data.to_pandas()
                                # Aggregate the data from this file
                                if aggregated_data is None:
                                    aggregated_data = file_data
                                else:
                                    aggregated_data = pd.concat([aggregated_data, file_data], ignore_index=True)

                                # Append the current state of aggregated data to the output file
                                # Ensure the output file path ends with a directory separator
                                output_file = os.path.join(output_file_path, "aggregated_data.parquet")
                                pq.write_table(pa.Table.from_pandas(aggregated_data), output_file)



# Usage:
#input_directory = r'C:\Users\200408\OneDrive - Betonmast\Skrivebord\NTNU\Prosjektoppgave\raw_parquetfiles'
#output_file_path = r'C:\Users\200408\OneDrive - Betonmast\Skrivebord\NTNU\Prosjektoppgave\raw_first_step'
#averaging_parquetfiles(input_directory, output_file_path)