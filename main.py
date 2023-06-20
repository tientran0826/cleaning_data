import re
import pandas as pd 
import numpy as np

def find_max_length(data):
    max_len = 0
    for line in data:
        line = re.sub(r'\([^)]*\)', '', line)[4:].replace(",", "").split()
        #print(len(line))
        if len(line) > max_len:
            max_len = len(line)
    return max_len

def clean_data(file_path):
    file = open(file_path, "r",encoding="utf-8")

    # Read the file line by line
    lines = file.readlines()

    # Close the file
    file.close()

    stock_datas = []

    max_len = find_max_length(lines)

    for line in lines:

        line = re.sub(r'\([^)]*\)', '', line)
        # Get stock name
        stock_name = line[:3]

        # Get stock data
        data = line[4:].replace(",", "").split()

        # If a line is missing columns
        if len(data) < max_len:
            # Fill column 9 with 0 value
            if data[-1].endswith("%"):
                data.insert(len(data)-1, 0)
            else:
            # Fill column 10 with "0%"
                data.insert(len(data), "0%")

        # Remove "%" in the last column
        data[-1] = str(data[-1])[:-1]

        # Add Stock Name to index 0
        data.insert(0,stock_name)
        stock_datas.append(data)

    output = pd.DataFrame(stock_datas)
    output.iloc[:,1] = pd.to_datetime(output.iloc[:,1], format='%d/%m/%Y')

    grouped_dataframes = {}
    for group_name, group_indices in output.groupby(by = 0).groups.items():
        # Get the group DataFrame
        group_df = output.loc[group_indices]
        
        reversed_df = group_df.sort_values(by = 1)

        for i in range(2,9):
            if i == 4:
                continue
            
            cumsum_value = reversed_df.iloc[:,i].astype('float64').cumsum()
            group_df.iloc[:,i] = cumsum_value[::-1]
        
        group_df.iloc[:,-1] = group_df.iloc[:,-1].astype('float64').replace(0, np.nan).fillna(method='backfill')
        group_df.iloc[:,-2] = group_df.iloc[:,-2].astype('float64').replace(0, np.nan).fillna(method='backfill')
        grouped_dataframes[group_name] = group_df

    for key,value in grouped_dataframes.items():
        pd.DataFrame(value).to_csv(f'{key}.csv',index=False)

file_path = "data17.txt"
clean_data(file_path=file_path)