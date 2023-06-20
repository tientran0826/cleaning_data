import re
import pandas as pd 
import numpy as np


def clean_data(file_path):
    file = open(file_path, "r",encoding="utf-8")

    # Read the file line by line
    lines = file.readlines()

    # Close the file
    file.close()

    stock_datas = []
    for line in lines:
        line = re.sub(r'\([^)]*\)', '', line)
        # Get stock name
        stock_name = line[:3]
        data = line[4:].replace(",", "").split()
        if len(data) == 9:
            if data[-1].endswith("%"):
                data.insert(8, 0)
            else:
                data.insert(9, "0%")
        data[-1] = str(data[-1])[:-1]

        stock_data = {
            "Co phieu" : stock_name,
            "Ngay": data[0],
            "KL giao dich rong": float(data[1]),
            "Gia tri giao dich rong": float(data[2]),
            "Thay doi": float(data[3]),
            "Khoi luong mua": float(data[4]),
            "Gia tri mua": float(data[5]),
            "Khoi luong ban": float(data[6]),
            "Gia tri ban": float(data[7]),
            "Room con lai": float(data[8]),
            "Dang so huu": float(data[9])
        }
        stock_datas.append(stock_data)

    output = pd.DataFrame(stock_datas)
    #output.to_csv("output.csv",index=False)
    output['Ngay'] = pd.to_datetime(output['Ngay'], format='%d/%m/%Y')

    grouped_dataframes = {}
    for group_name, group_indices in output.groupby('Co phieu').groups.items():
        # Get the group DataFrame
        group_df = output.loc[group_indices]
        # Store the group DataFrame in the dictionary
        
        reversed_df = group_df.sort_values('Ngay')

        buy_volume = reversed_df['Khoi luong mua'].cumsum()
        buy_value = reversed_df['Gia tri mua'].cumsum()

        sell_volume = reversed_df['Khoi luong ban'].cumsum()
        sell_value = reversed_df['Gia tri ban'].cumsum()

        net_volume = reversed_df['KL giao dich rong'].cumsum()
        net_value = reversed_df['Gia tri giao dich rong'].cumsum()

        group_df['Khoi luong mua'] = buy_volume[::-1]
        group_df['Gia tri mua'] = buy_value[::-1]

        group_df['Khoi luong ban'] = sell_volume[::-1]
        group_df['Gia tri ban'] = sell_value[::-1]

        group_df['Room con lai'] = group_df['Room con lai'].replace(0, np.nan).fillna(method='backfill')
        group_df['Dang so huu'] = group_df['Dang so huu'].replace(0, np.nan).fillna(method='backfill')

        group_df['KL giao dich rong'] = net_volume[::-1]
        group_df['Gia tri giao dich rong'] = net_value[::-1]

        grouped_dataframes[group_name] = group_df

    for key,value in grouped_dataframes.items():
        pd.DataFrame(value).set_index('Ngay').to_csv(f'{key}.csv')

file_path = "data17.txt"
clean_data(file_path=file_path)