# -*- coding: utf-8 -*-

# Import necessary libraries
import os
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import json
import csv

# 将科学计数法的精度设置为0
pd.set_option('display.float_format', lambda x: '%.0f' % x)

# Set the path to the directory containing the data files
path = r"/GPUFS/njnu_ynwen_1/PVNB/week1"

# Create empty lists to store the data
result = []
lst = []
lst2 = []

# Define a function to find all the Excel files in the directory and its subdirectories
def findfiles(path):
    # Get a list of all the files and directories in the path
    file_list = os.listdir(path)
    # Loop through the list
    for file in file_list:
        # Get the full path of the current item
        cur_path = os.path.join(path, file)
        # Check if the current item is a directory
        if os.path.isdir(cur_path):
            # If it is, call the function recursively with the new path
            findfiles(cur_path)
        else:
            # If it is not a directory, check if it is an Excel file
            if '.xlsx' in file:
                # If it is, add its full path to the result list
                result.append(os.path.join(path, file))

# Call the findfiles function to get a list of all the Excel files in the directory and its subdirectories
findfiles(path)

# Loop through the Excel files in the result list
for i in result:
    # Load the data from the 'information' column of the Excel file into a pandas DataFrame
    sj = pd.read_excel(i)['information']
    # Loop through the rows of the DataFrame
    for j in sj:
        try:
            # Try to decode the JSON data in the row
            text = json.loads(j)['data']
        except json.decoder.JSONDecodeError:
            # If decoding fails, skip the row
            continue
        # Add the filename (without the extension) as a '时间' column to the JSON data
        try:
            text['时间'] = i.split('\\')[-1].split('.')[0]
        except:
            continue

        # Append the JSON data to the 'lst' list
        lst.append(text)

# Create a pandas DataFrame from the 'lst' list
hj = pd.DataFrame(lst)

# Create an empty list to store the data for the final output
lst2 = []

# Loop through the rows of the 'hj' DataFrame
for m in range(len(hj)):
    # Get the 'id', 'name', and 'pileDetailsList' columns for the current row
    sid = hj['id'].loc[m]
    sname = hj['name'].loc[m]
    text1 = hj['pileDetailsList'].loc[m]
    # Loop through the rows of the 'pileDetailsList' column
    for n in range(len(text1)):
        # Create a dictionary to store the data for the current row
        data={}
        # Add the 'id', 'name', and '时间' columns from the 'hj' DataFrame to the dictionary
        data['充电站id'] = sid
        data['时间'] = hj['时间'].loc[m]
        # Add the 'pileNo', 'statusStr', and 'power' columns from the 'pileDetailsList' column to the dictionary
        data['充电桩id'] = str(text1[n]['pileNo'])
        data['状态'] = text1[n]['statusStr']
        data['功率'] = text1[n]['power']
        # Append the dictionary to the 'lst2' list
        lst2.append(data)

# Create a pandas DataFrame from
result2 = pd.DataFrame(lst2)

# # 统计充电桩使用情况
# tj1 = pd.pivot_table(result2, index=['时间','充电桩id'], columns=['状态'], aggfunc='count')
# tj1 = tj1.reset_index()
# tj1.to_csv('result1.csv', index=False, encoding= 'utf-8-sig')
tj2 = pd.pivot_table(result2, index=['充电站id', '功率'], columns=['状态'], aggfunc='count')
tj2 = tj2.reset_index()
print(tj2)
tj2.to_csv('week1.csv', index=False, encoding= 'utf-8-sig')
# 根据需求重命名列名
# columns = []
# ls = len(tj2.columns)
# for i in range(ls):
#     columns.append(tj2.columns[i][1])
# columns[0] = '充电桩id'
# tj2.columns = columns

# columns = []
# ls = len(tj1.columns)
# for i in range(ls):
#     columns.append(tj1.columns[i][1])
# columns[1] = '充电桩id'
# tj1.columns = columns

# # 删除无用列并去重
# del hj['pileDetailsList']
# #del hj['时间']
# hj.drop_duplicates(subset=['id'], keep='first', inplace=True)
# # 合并表格并输出到CSV文件
# tj2.rename(columns={'充电桩id': 'id'}, inplace=True)
# tj3 = pd.concat([tj2, hj[['id']]], axis=1)
# tj3.drop_duplicates(subset=['id'], keep='first', inplace=True)
# tj3.to_csv('result.csv', index=False, encoding= 'utf-8-sig')


