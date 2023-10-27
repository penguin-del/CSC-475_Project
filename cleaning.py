# -*- coding: utf-8 -*-
"""
@name: cleaning.py
@desc: this file cleans the downloaded data from import.py
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
folder_path = 'C:\\Users\jrhut\OneDrive\Documents\Computer Science\CSC-475\CSC-475_Project'  
for county in code_list:
    file_name = "all_data_employment_%s.csv" % county  # Replace with the name of the file you want to check
    file_path = os.path.join(folder_path, file_name)
    if not os.path.isfile(file_path):
        missed.append(county)
#print(missed)

#####################################################################################################
################################ Section 1: Inflation ###############################################
#####################################################################################################

# The inflation data set is already in one file, we just need to clean it
# Define the BLS encodings into dictionaries 
inflation = pd.read_csv("all_data_inflation.csv")
region_dictionary = {"0": "USA", "1": "Northeast", "2": "Midwest", "3": "South", "4": "West"}
product_dictionary = {"SAF111": "Cereals/Wheat",
                      "SAF112": "Meat",
                      "SAF113": "Fruit and Vegetable",
                      "SAF114": "Non-alcoholic Beverages",
                      "SEFJ": "Dairy",
                      "SAH": "Housing",
                      "SEFV": "Eating Out",
                      "SAH21": "Household Energy",
                      "SAA": "Clothes\Apparel",
                      "SS4501A": "New Cars",
                      "SETA02": "Used Cars",
                      "SETB01": "Gasoline",
                      "SAM1": "Medical Commodities",
                      "SAM2": "Medical Services",
                      "SEEB": "Tuition"
                        }
# Define the region for each instance
inflation["Region"] = inflation["seriesID"].str[5]
inflation["Region"] = inflation["Region"].replace(region_dictionary)

# Define the product type for each instance
inflation["Product"] = inflation["seriesID"].str[8:]
inflation["Product"] = inflation["Product"].replace(product_dictionary)

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
county_dict = county_data.set_index('Code').to_dict()['Area Title']
use_dict = {'3': 'Unemployment Rate', '6': 'Labor Force Size'}

# Define the county for each instance
unemployment["County"] = unemployment["seriesID"].str[5:10]
unemployment["County"] = unemployment["County"].replace(county_dict)

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
industry_dict = {"1011": "Natural Resources and Mining",
                 "1012": "Construction",
                 "1013": "Manufacturing",
                 "1021": "Trade, Transportation, and Utilities",
                 "1022": "Information",
                 "1023": "Financial Activities",
                 "1024": "Professional and Business Services",
                 "1025": "Education and Health Services",
                 "1026": "Leisure and Hospitality",
                 "1027": "Other Services",
                 "1028": "Public Administration",
                 "1029": "Unclassified"}
type_dict = {'105': 'Employment', '405': 'Wages'}

# For each of the counties, import the respective csv if it exists and add it to the larger data frame.
for county in code_list:
    file_name = "all_data_employment_%s.csv" % county
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        temp = pd.read_csv(file_path)
        employment = pd.concat([employment, temp])

# Define the county for each instance
employment["County"] = employment["seriesID"].str[3:8]
employment["County"] = employment["County"].replace(county_dict)

# Define the industry for each instance
employment["Industry"] = employment["seriesID"].str[-4:]
employment["Industry"] = employment["Industry"].replace(industry_dict)

# Define the data type for each instance (either employment or wages)
employment["Type"] = employment["seriesID"].str[-7:-4]
employment["Type"] = employment["Type"].replace(type_dict)

# Drop the unnecessary column, rename the remaining ones, and export to a csv
employment = employment.drop('Unnamed: 0', axis=1)
employment = employment.rename(columns={'seriesID': 'ID', 'year': 'Year', 'period': 'Period', 'value': 'Value'})
employment.to_csv("all_data_employment_cleaned.csv")
    
    
    
