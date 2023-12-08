# -*- coding: utf-8 -*-
"""
@name: cleaning.py
@desc: This file cleans the downloaded data from import.py
@date: October 18th, 2023
@author: Joshua Hutson
"""
import pandas as pd
import os

#Count which counties were not downloaded
file_path = 'County_Codes.xlsx'
county_data = pd.read_excel(file_path, sheet_name= "Full List", converters={'Code': lambda x: f"{x:05}"})

# Convert the 'Code' column to a list
code_list = county_data['Code'].tolist()

#Check for each county that there is a corresponding data set. If not, add it to the list
missed = []
folder_path = 'C:\\Users\jrhut\OneDrive\Documents\Computer Science\CSC-475'  
for county in code_list:
    file_name = "all_data_employment_%s.csv" % county  # Replace with the name of the file you want to check
    file_path = os.path.join(folder_path, file_name)
    if not os.path.isfile(file_path):
        missed.append(county)

#####################################################################################################
################################ Section 1: Inflation ###############################################
#####################################################################################################

# The inflation data set is already in one file, we just need to clean it
# Define the BLS encodings into dictionaries 
inflation = pd.read_csv("C:\\Users\jrhut\OneDrive\Documents\Computer Science\CSC-475\\all_data_inflation.csv")
month_dictionary = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
# Define the region for each instance
inflation["Region"] = inflation["seriesID"].str[5]
#inflation["Region"] = inflation["Region"].replace(region_dictionary)

# Define the product type for each instance
inflation["Product"] = inflation["seriesID"].str[8:]
#inflation["Product"] = inflation["Product"].replace(product_dictionary)

inflation["month"] = inflation["month"].replace(month_dictionary)
inflation['Date'] = pd.to_datetime(inflation['year'].astype(str) + inflation['month'].astype(str), format='%Y%m') + pd.offsets.MonthBegin(1)

# Drop an unnecessary column, rename the other columns, and export as a csv
inflation = inflation.drop('Unnamed: 0', axis=1)
inflation = inflation.rename(columns={'seriesID': 'ID', 'year': 'Year', 'month': 'Month', 'value': 'CPI value'})
inflation.to_csv("all_data_inflation_cleaned.csv")

#####################################################################################################
################################ Section 2: Unemployment ############################################
#####################################################################################################

# The unemployment data set is separated by numbers (1-128) so we can compile them 
# using a for loop
unemployment = pd.read_csv("all_data_unemployment_1.csv")
for i in range(2, 129):
    temp = pd.read_csv("all_data_unemployment_%s.csv" % i)
    unemployment = pd.concat([unemployment, temp])

# Create a dictionary from the county codes and data types
# county_dict = county_data.set_index('Code').to_dict()['Area Title']
use_dict = {'3': 1, '6': 2} #For data storage reasons, we will make unemployment rate 1 and labor force size 2

#Rename the months as integers for less data storage problems
unemployment["month"] = unemployment["month"].replace(month_dictionary)
unemployment['Date'] = pd.to_datetime(unemployment['year'].astype(str) + unemployment['month'].astype(str), format='%Y%m') + pd.offsets.MonthBegin(1)

# Define the county for each instance
unemployment["County"] = unemployment["seriesID"].str[5:10]
#unemployment["County"] = unemployment["County"].replace(county_dict)

# Define the data type for each instance
unemployment["Type"] = unemployment["seriesID"].str[-1]
unemployment["Type"] = unemployment["Type"].replace(use_dict)

#Drop an unecessary column, rename the other columns, and export as a csv
unemployment = unemployment.drop('Unnamed: 0', axis=1)
unemployment = unemployment.rename(columns={'seriesID': 'ID', 'year': 'Year', 'month': 'Month', 'value': 'Value'})
unemployment.to_csv("all_data_unemployment_cleaned.csv")

#####################################################################################################
################################ Section 3: Employment ##############################################
#####################################################################################################

# The employment data set is separated by county. Given that we decided to overlook Alaska,
# and three other counties simply do not have data, we will have to handle those exceptions.

# Define each BLS industry encoding in a dictionary.
employment = pd.DataFrame()
type_dict = {'105': 1, '405': 2} #Rename employment numbers as 1 and wages as 2
period_dictionary = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12,
                    "1st Quarter": 1, "2nd Quarter": 4, "3rd Quarter": 7, "4th Quarter": 10}

# For each of the counties, import the respective csv if it exists and add it to the larger data frame.
for county in code_list:
    file_name = "all_data_employment_%s.csv" % county
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        temp = pd.read_csv(file_path)
        employment = pd.concat([employment, temp])

# Define the county for each instance
employment["County"] = employment["seriesID"].str[3:8]
#employment["County"] = employment["County"].replace(county_dict)

# Define the industry for each instance
employment["Industry"] = employment["seriesID"].str[-4:].astype(int)
#employment["Industry"] = employment["Industry"].replace(industry_dict)

# Define the data type for each instance (either employment or wages)
employment["Type"] = employment["seriesID"].str[-7:-4]
employment["Type"] = employment["Type"].replace(type_dict)

employment["period"] = employment["period"].replace(period_dictionary)
employment["Date"] = pd.to_datetime(employment['year'].astype(str) + employment['period'].astype(str), format='%Y%m') + pd.offsets.MonthBegin(1)

# Drop the unnecessary column, rename the remaining ones, and export to a csv
employment = employment.drop('Unnamed: 0', axis=1)
employment = employment.rename(columns={'seriesID': 'ID', 'year': 'Year', 'period': 'Period', 'value': 'Value'})
employment.to_csv("all_data_employment_cleaned.csv")
    
    
## Retry Unemployment
file_1 = "all_data_unemployment_retry_1.csv"
file_2 = "all_data_unemployment_retry_2.csv"

temp = pd.read_csv(file_1)
retry_unemployment = pd.read_csv(file_2)
retry_unemployment = pd.concat([temp, retry_unemployment])

retry_unemployment["month"] = retry_unemployment["month"].replace(month_dictionary)
retry_unemployment['Date'] = pd.to_datetime(retry_unemployment['year'].astype(str) + retry_unemployment['month'].astype(str), format='%Y%m') + pd.offsets.MonthBegin(1)
retry_unemployment["County"] = retry_unemployment["seriesID"].str[5:10]
retry_unemployment["Type"] = retry_unemployment["seriesID"].str[-1]
retry_unemployment = retry_unemployment.drop('Unnamed: 0', axis=1)
retry_unemployment = retry_unemployment.rename(columns={'seriesID': 'ID', 'year': 'Year', 'month': 'Month', 'value': 'Value'})
retry_unemployment.to_csv("all_data_unemployment_retry_cleaned.csv")

## Retry Employment
employment_retry = pd.DataFrame()
folder_path_2 = 'C:\\Users\jrhut\OneDrive\Documents\Computer Science\CSC-475\CSC-475_Project'
county_data = pd.read_excel('County_Codes.xlsx', sheet_name= "States", converters={'Code': lambda x: f"{x:05}"})
state_list  = county_data['Code'].tolist()
for state in state_list:
    file_name = "all_data_employment_retry_%s.csv" % state
    file_path = os.path.join(folder_path_2, file_name)
    if os.path.isfile(file_path):
        temp = pd.read_csv(file_path)
        employment_retry = pd.concat([employment_retry, temp])


employment_retry["County"] = employment_retry["seriesID"].str[3:8]
employment_retry["Industry"] = employment_retry["seriesID"].str[-4:].astype(int)
employment_retry["Type"] = employment_retry["seriesID"].str[-7:-4]
employment_retry["period"] = employment_retry["period"].replace(period_dictionary)
employment_retry["Date"] = pd.to_datetime(employment_retry['year'].astype(str) + employment_retry['period'].astype(str), format='%Y%m') + pd.offsets.MonthBegin(1)
employment_retry = employment_retry.drop('Unnamed: 0', axis=1)
employment_retry = employment_retry.rename(columns={'seriesID': 'ID', 'year': 'Year', 'period': 'Period', 'value': 'Value'})
employment_retry.to_csv("all_data_employment_retry_cleaned.csv")



    
