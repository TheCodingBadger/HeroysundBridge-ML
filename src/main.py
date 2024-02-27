import data_processing.modules.mat2parquet as mat2parquet
import data_processing.modules.parquet_add_date as parquet_add_date
import data_processing.parquet_avg as parquet_avg

import os
import sys
import tensorflow as tf
import polars as pl 

# Get the assets folder
asset_folder = os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..', 'HeroysundBridge-ML-Assets'))

# Inputs
#year = "2023"
#
#
#folder  = os.path.dirname#(os.path.dirname(os.path.dirname(os.path.dirname(sys.executable)))) 
#print(folder)
# year_folder_mat = os.path.join(folder, year)
# year_folder_parquet = year_folder_mat + "_parquet"
# month_folder_parquet = year_folder_parquet + "_monthly"
# spesific_path = r'C:\Users\200408\OneDrive - Betonmast\Skrivebord\NTNU\Prosjektoppgave\Averages\aggregated_data.parquet'
# spesific_path1 = r'C:\Users\200408\repos\aggregated_data.parquet'
# 
# input_directory = r'C:\Users\200408\OneDrive - Betonmast\Skrivebord\NTNU\Prosjektoppgave\raw_first_step'
# output_directory = r'C:\Users\200408\OneDrive - Betonmast\Skrivebord\NTNU\Prosjektoppgave\Averages'

### Code ###
## Code for making procressing and combining both sensor and weater data

# Step 1: Convert .mat-files to .parquet-files
#ut.saveMatAsParquet(year_folder_mat, year_folder_parquet)

# Step 2: Add columns to the .parquet-files
#cr.adding_date_filename_parquet(input_directory, output_directory)

# Step 3: Average the .parquet-files
#Avg.averaging_parquetfiles(input_directory, output_directory)

# Step 4: Use the nnotebook file "Processing climate data" to process the weater data
# Step 5: Use the nnotebook file "Combining sensor and weather data" to process the traffic data


# parquet_files = [os.path.join(spesific_path, f) for f in os.listdir(spesific_path) if f.endswith('.parquet')][:100]
# dfs = [pl.read_parquet(f) for f in parquet_files]
# for i, df in enumerate(dfs):
#    print(f"Shape of file {i+1}: {df.shape}")

# print(folder)
# print(year_folder_mat)
# print(year_folder_parquet)
# print(month_folder_parquet)

#print(tf.__version__)
#data = pl.read_parquet(r'C:\Users\erlin\repos\Average_per_minute.parquet')
#print(data)