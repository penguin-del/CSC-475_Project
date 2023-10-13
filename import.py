# -*- coding: utf-8 -*-
"""
@name: import.py
@desc: this file imports a JSON library to import data from the Bureau of Labor Statistics API
@date: October 3rd, 2023
@author: Joshua Hutson
"""
    
import pandas as pd
import requests
import json
import time

#The following code is from the BLS API website

headers = {'Content-type': 'application/json'}
#Northwest: 100, Midwest: 200, South: 300, Midwest: 400
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
                                  'CUUR0400SAM2', 'CUUR0400SEEB', 'LAUCN010010000000003', 'LAUCN010010000000004' , 'LAUCN010010000000005', 'LAUCN010010000000006'],
                     "registrationkey":"e836f8531fca42e7a41c7ab551f6778a","startyear":"2014", "endyear":"2023", "calculations":True})

p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
q = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data_2, headers=headers)

json_data = json.loads(p.text)
json_data_2 = json.loads(q.text)


json_files = [json_data, json_data_2]
results = []
for file in json_files:
    for series in json_data['Results']['series']:
      seriesId = series['seriesID']
      for item in series['data']:
          year = item['year']
          period = item['periodName']
          value = item['value']
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
          
          results.append([seriesId,year,period,value,pct_1mth,pct_3mth,pct_6mth,pct_12mth])
df = pd.DataFrame(results)
df.columns = ['seriesID', 'year', 'month', 'value', 'One Month Percent Change', 'Three Month Percent Change', 'Nine Month Percent Change', 'Twelve Month Percent Chagne']

print (df)
df.to_csv("all_data_inflation.csv")


##### Employment Data Imports ########
file_path = 'County Codes.xlsx'

# Read the Excel file into a DataFrame
county_data = pd.read_excel(file_path, converters={'Code': lambda x: f"{x:05}"})

# Convert the 'Code' column to a list
code_list = ['01001', '01003', '01005', '01007', '01009']
#code_list = county_data['Code'].tolist()
industry_list = ['1011','1012', '1013', '1021',
                 '1022', '1023', '1024', '1025',
                 '1026', '1027', '1028', '1029']
data_type_list = ['105', '405']

#Loop through this list of counties
employ_wage_data = pd.DataFrame(columns = ['seriesID', 'year', 'period', 'value'])

for county in code_list:
    time.sleep(0.2)
    for dtype in data_type_list:
        series_list = []
        for industry in industry_list:
            series_list.append('ENU'+ county + dtype + industry)
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": series_list,"startyear":"2014", "endyear":"2023"})
    p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    results = []
    if 'series' in json_data['Results']:
        for series in json_data['Results']['series']:
          seriesId = series['seriesID']
          for item in series['data']:
              year = item['year']
              period = item['period']
              value = item['value']
              results.append([seriesId,year,period,value])
        temp = pd.DataFrame(results)
        temp.columns = ['seriesID', 'year', 'period', 'value']
        employ_wage_data = pd.concat([temp, employ_wage_data])
            
    employ_wage_data.to_csv("all_data_employment_%s.csv" % county)
type(json_data)


#Unemployment data set


data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df1 = pd.DataFrame(data)

# Create an empty DataFrame
df2 = pd.DataFrame(columns=['A', 'B'])

# Concatenate the empty DataFrame to the non-empty one vertically
result = pd.concat([df1, df2])

print(result)


