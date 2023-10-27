# -*- coding: utf-8 -*-
"""
@name: import.py
@desc: this file imports a JSON library to import data from the Bureau of Labor Statistics API
@date: October 3rd, 2023
@author: Joshua Hutson
"""
<<<<<<< HEAD
<<<<<<< HEAD
    
import pandas as pd
import requests
import json
import time

#The following code was modified from the BLS API website (expires in October 2024)

##### API keys: expire in October 2024
#1. e836f8531fca42e7a41c7ab551f6778a
#2. 273fc78876ad47e88fbc331be1ee5fb9
#3. e061f1ef9cce400b994fd80c56df7bc4
#4. 9ec4db91d4284d579810102d12bfddef

#####################################################################################################
################################ Section 1: Inflation ###############################################
#####################################################################################################

# Define Headers for all imports
headers = {'Content-type': 'application/json'}


# Collect data by listing the relevant serieses
data = json.dumps({"seriesid": ['CUUR0100SAF111', 'CUUR0100SAF112', 'CUUR0100SAF113', 'CUUR0100SAF114',
                                'CUUR0100SEFJ', 'CUUR0100SAH', 'CUUR0100SEFV', 'CUUR0100SAH21', 'CUUR0100SAH21',
                                'CUUR0100SAA', 'CUUR0100SS4501A', 'CUUR0100SETA02', 'CUUR0100SETB01', 'CUUR0100SAM1',
                                'CUUR0100SAM2', 'CUUR0100SEEB', 'CUUR0200SAF111', 'CUUR0200SAF112', 'CUUR0200SAF113', 'CUUR0200SAF114',
                                'CUUR0200SEFJ', 'CUUR0200SAH', 'CUUR0200SEFV', 'CUUR0200SAH21', 'CUUR0200SAH21',
                                'CUUR0200SAA', 'CUUR0200SS4501A', 'CUUR0200SETA02', 'CUUR0200SETB01', 'CUUR0200SAM1',
                                'CUUR0200SAM2', 'CUUR0200SEEB', 'CUUR0300SAF111', 'CUUR0300SAF112', 'CUUR0300SAF113', 'CUUR0300SAF114',
                                'CUUR0300SEFJ', 'CUUR0300SAH', 'CUUR0300SEFV', 'CUUR0300SAH21', 'CUUR0300SAH21',
                                'CUUR0300SAA', 'CUUR0300SS4501A', 'CUUR0300SETA02', 'CUUR0300SETB01', 'CUUR0300SAM1',
                                'CUUR0300SAM2', 'CUUR0300SEEB', 'CUUR0400SAF111', 'CUUR0400SAF112'],
                   "registrationkey":"e836f8531fca42e7a41c7ab551f6778a", "startyear":"2004", "endyear":"2023", "calculations":True})
data_2 = json.dumps({"seriesid": ['CUUR0400SAF113', 'CUUR0400SAF114','CUUR0400SEFJ', 'CUUR0400SAH', 
                                  'CUUR0400SEFV', 'CUUR0400SAH21', 'CUUR0400SAH21','CUUR0400SAA', 
                                  'CUUR0400SS4501A', 'CUUR0400SETA02', 'CUUR0400SETB01', 'CUUR0400SAM1',
                                  'CUUR0400SAM2', 'CUUR0400SEEB','CUUR0400SAH', 'CUUR0400SEFV', 'CUUR0400SAH21', 'CUUR0400SAH21',
                                  'CUUR0400SAA', 'CUUR0400SS4501A', 'CUUR0400SETA02', 'CUUR0400SETB01', 'CUUR0400SAM1',
                                  'CUUR0400SAM2', 'CUUR0400SEEB', 'CUUR0000SAF111', 'CUUR0000SAF112',
                                  'CUUR0000SAF113', 'CUUR0000SAF114','CUUR0000SEFJ', 'CUUR0000SAH', 
                                  'CUUR0000SEFV', 'CUUR0000SAH21', 'CUUR0000SAH21','CUUR0000SAA', 
                                  'CUUR0000SS4501A', 'CUUR0000SETA02', 'CUUR0000SETB01', 'CUUR0000SAM1',
                                  'CUUR0000SAM2', 'CUUR0000SEEB','CUUR0000SAH', 'CUUR0000SEFV', 'CUUR0000SAH21', 'CUUR0000SAH21',
                                  'CUUR0000SAA', 'CUUR0000SS4501A', 'CUUR0000SETA02', 'CUUR0000SETB01', 'CUUR0000SAM1',
                                  'CUUR0000SAM2', 'CUUR0000SEEB'],
                     "registrationkey":"e836f8531fca42e7a41c7ab551f6778a","startyear":"2004", "endyear":"2023", "calculations":True})

# Request the series
p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
q = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data_2, headers=headers)

#Get the data
json_data = json.loads(p.text)
json_data_2 = json.loads(q.text)

# For each set of series' import relevant data
json_files = [json_data, json_data_2]
results = []
for file in json_files:
    for series in file['Results']['series']:
      seriesId = series['seriesID'] # Get the table ID
      for item in series['data']:
          year = item['year'] # Get the year
          period = item['periodName'] # Get the name of the month
          value = item['value'] # Get the CPI value for the month and year
          
          # Get percent change in CPI for the last month, three months, six months, and year
          if 'calculations' in item:
              if '1' in item['calculations']['pct_changes']: pct_1mth = item['calculations']['pct_changes']['1']
              else: pct_1mth = ''
              if '3' in item['calculations']['pct_changes']: pct_3mth = item['calculations']['pct_changes']['3']
              else: pct_3mth = ''
              if '6' in item['calculations']['pct_changes']: pct_6mth = item['calculations']['pct_changes']['6']
              else: pct_6mth = ''
              if '12' in item['calculations']['pct_changes']: pct_12mth = item['calculations']['pct_changes']['12']
              else: pct_12mth = ''
             
          # If the calculations do not exist, make the value blank
          else: 
              pct_1mth = ''
              pct_3mth = ''
              pct_6mth = ''
              pct_12mth = ''
          
            # Append this set of results to the list at large
          results.append([seriesId,year,period,value,pct_1mth,pct_3mth,pct_6mth,pct_12mth])
# Export the results as a csv
df = pd.DataFrame(results)
df.columns = ['seriesID', 'year', 'month', 'value', 'One Month Percent Change', 'Three Month Percent Change', 'Nine Month Percent Change', 'Twelve Month Percent Chagne']
df.to_csv("all_data_inflation.csv")

############################################################################
################### Section 2: Employment ##################################
############################################################################

# Read the county code Excel file into a DataFrame
file_path = 'County_Codes.xlsx'
county_data = pd.read_excel(file_path, sheet_name= "Sixth 500", converters={'Code': lambda x: f"{x:05}"})

# Convert the 'Code' column to a list
code_list = county_data['Code'].tolist()

# Define the industries to import and the data to import
industry_list = ['1011','1012', '1013', '1021',
                 '1022', '1023', '1024', '1025',
                 '1026', '1027', '1028', '1029']
data_type_list = ['105', '405'] # 105 = number of employees, 405 = average weekly wage

#Loop through this list of counties
for county in code_list:
    time.sleep(0.2)
    series_list = []
    
    # Create a list of series's using data type and industry codes (for each county)
    for dtype in data_type_list:
        for industry in industry_list:
            series_list.append('ENU'+ county + dtype + industry)
    
    # Get the data from the BLS website.
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": series_list, "registrationkey":"e061f1ef9cce400b994fd80c56df7bc4", "startyear":"2004", "endyear":"2023", "calculations":True})
    p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    
    # For each of the series we downloaded, get the right data and put it into a list.
    results = []
    if 'series' in json_data['Results']:
        for series in json_data['Results']['series']:
          seriesId = series['seriesID'] # Table ID
          for item in series['data']:
              year = item['year'] # Year
              period = item['periodName'] # Either month or quarter
              value = item['value'] # Either number of employees or average wages
              
              # If the percent change calculations for 1, 3, 6, and 12 months exist, get them
              if 'calculations' in item:
                  if '1' in item['calculations']['pct_changes']: pct_1mth = item['calculations']['pct_changes']['1']
                  else: pct_1mth = ''
                  if '3' in item['calculations']['pct_changes']: pct_3mth = item['calculations']['pct_changes']['3']
                  else: pct_3mth = ''
                  if '6' in item['calculations']['pct_changes']: pct_6mth = item['calculations']['pct_changes']['6']
                  else: pct_6mth = ''
                  if '12' in item['calculations']['pct_changes']: pct_12mth = item['calculations']['pct_changes']['12']
                  else: pct_12mth = ''
              else: 
                  pct_1mth = ''
                  pct_3mth = ''
                  pct_6mth = ''
                  pct_12mth = ''
            
              # Add the new data to the list
              results.append([seriesId,year,period,value,pct_1mth,pct_3mth,pct_6mth,pct_12mth])
              
    # Export all of the data to a csv file for the county
    temp = pd.DataFrame(results)
    temp.columns = ['seriesID', 'year', 'period', 'value', 'One Month Percent Change', 'Three Month Percent Change', 'Nine Month Percent Change', 'Twelve Month Percent Chagne']    
    temp.to_csv("all_data_employment_%s.csv" % county)


############################################################################
######################## Section 3: Unemployment ###########################
############################################################################


# Read the county codes again and make a list out of them
county_data = pd.read_excel(file_path, converters={'Code': lambda x: f"{x:05}"})
code_list = county_data['Code'].tolist()

data_type_list = ['3', '6'] #3 is for the unemployment rate and 6 is for the labor force size

#Loop through this list of counties
marker = 0
series_list = []
for county in code_list:
    time.sleep(0.2)
    
    # Only place 50 tables in each query
    if len(series_list) <= 48:
        for dtype in data_type_list:
            series_list.append('LAUCN'+ county + '000000000' + dtype)
            
    #When we have 50 tables, query the database
    else:
        marker += 1
        headers = {'Content-type': 'application/json'}
        data = json.dumps({"seriesid": series_list,"registrationkey":"e836f8531fca42e7a41c7ab551f6778a", "startyear":"2004", "endyear":"2023", "calculations":True})
        p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
        json_data = json.loads(p.text)
        
        # For each of the series we downloaded, get the right data and put it into a list.
        results = []
        if 'series' in json_data['Results']:
            for series in json_data['Results']['series']:
              seriesId = series['seriesID'] #Table ID
              for item in series['data']:
                  year = item['year'] #Year
                  period = item['periodName'] #Month
                  value = item['value'] #Either unemployment rate or labor force size.
                  
                  # If the percent change calculations for 1, 3, 6, and 12 months exist, get them
                  if 'calculations' in item:
                      if '1' in item['calculations']['pct_changes']: pct_1mth = item['calculations']['pct_changes']['1']
                      else: pct_1mth = ''
                      if '3' in item['calculations']['pct_changes']: pct_3mth = item['calculations']['pct_changes']['3']
                      else: pct_3mth = ''
                      if '6' in item['calculations']['pct_changes']: pct_6mth = item['calculations']['pct_changes']['6']
                      else: pct_6mth = ''
                      if '12' in item['calculations']['pct_changes']: pct_12mth = item['calculations']['pct_changes']['12']
                      else: pct_12mth = ''
                  else: 
                      pct_1mth = ''
                      pct_3mth = ''
                      pct_6mth = ''
                      pct_12mth = ''
                
                  # Add the new data to the list
                  results.append([seriesId,year,period,value,pct_1mth,pct_3mth,pct_6mth,pct_12mth])
        
        # Export the data to a csv file
        temp = pd.DataFrame(results)
        temp.columns = ['seriesID', 'year', 'month', 'value', 'One Month Percent Change', 'Three Month Percent Change', 'Nine Month Percent Change', 'Twelve Month Percent Chagne']     
        temp.to_csv("all_data_unemployment_%s.csv" % marker)
        
        #Ensure that we empty the series list and add the series associated with this iteration
        series_list = []
        for dtype in data_type_list:
            series_list.append('LAUCN'+ county + '000000000' + dtype)
    


=======

>>>>>>> parent of b00b8e2 (First skeleton outline for the Dashboard Website)
=======

>>>>>>> parent of b00b8e2 (First skeleton outline for the Dashboard Website)
