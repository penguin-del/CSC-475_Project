# -*- coding: utf-8 -*-
"""
@name: visualization.py
@desc: This file visualizes the cleaned Data from cleaning.py
@date: October 19th, 2023
@author: Joshua Hutson
"""

from bokeh.io.output import output_file
import pandas as pd
from bokeh.models import ColumnDataSource, Select, CustomJS, DateRangeSlider, LogColorMapper, TabPanel, Tabs, LinearColorMapper, ColorBar
from bokeh.plotting import figure, show
from bokeh.layouts import column, row
from datetime import date
from bokeh.sampledata.us_states import data as us_states
from bokeh.palettes import YlGnBu9 as YlGnBu
import numpy as np

########################################################################################
#################### Inflation Visualization Line Plot #################################
########################################################################################

#Define a dictionary of replacement values
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
region_dictionary = {0: "USA", 1: "Northeast", 2: "Midwest", 3: "South", 4: "West"}

# Load your data
data = pd.read_csv("all_data_inflation_cleaned.csv")
data = data.drop('Unnamed: 0', axis=1)
data['Product'] = data['Product'].replace(product_dictionary)
data['Region']  = data['Region'].replace(region_dictionary)

data['Date']= pd.to_datetime(data['Date'])
data = data.sort_values("Date")


# Initial data (defined from 2019 to 2023 without the USA as a whole)
# Percent Change Stats would not work if we started earlier than 2019.
initial_data = data[(data['Year'] >= 2019) & (data['Region'] != "USA")]

# Column Source initialization (this one will be updated by the JavaScript Code)
source = ColumnDataSource(data = dict(
        Date       = initial_data['Date'].values,
        metric     = initial_data['CPI value'].values,
        Product    = initial_data['Product'].values,
        Region     = initial_data['Region'].values
  ))

# Column Source initialization (this one will be the reference to update the original)
backup = ColumnDataSource(data = dict(
        Date       = initial_data['Date'].values,
        CPI        = initial_data['CPI value'].values,
        One_Month_Percent_Change = initial_data['One Month Percent Change'].values,
        Three_Month_Percent_Change = initial_data['Three Month Percent Change'].values,
        Six_Month_Percent_Change = initial_data['Nine Month Percent Change'].values,
        Twelve_Month_Percent_Change = initial_data['Twelve Month Percent Chagne'].values,
        Product    = initial_data['Product'].values,
        Region     = initial_data['Region'].values
  ))

# Initialize the figure itself
p = figure(x_axis_type = "datetime", x_axis_label="Date", y_axis_label="Value", \
           width = 1200, height = 550)

#Add the line to the figure
p.line('Date', 'metric', source=source, line_width = 3)

# Create a dropdown menu for the Product
product_select = Select(title="Select a Product:", \
                        value="Cereals/wheat", \
                        options=list(initial_data['Product'].unique()))

# Create a dropdown menu for the Region
region_select  = Select(title="Select a Region:", \
                        value="Midwest", \
                        options=list(initial_data['Region'].unique()))

# Create a dropdown menu for the Metric
metric_select  = Select(title="Select a Metric:", \
                        value="CPI", \
                        options=["CPI", "One_Month_Percent_Change", "Three_Month_Percent_Change", "Six_Month_Percent_Change", "Twelve_Month_Percent_Change"])

# Create a date slider
Date_slider = DateRangeSlider(value=(date(2019, 1, 1), date(2023, 10, 1)),
                                    start=date(2019, 1, 1), end=date(2023, 10, 1))

# JavaScript Code to update the visualization dynamically
callback = CustomJS(args=dict(source=source, \
                               backup = backup, \
                               p_val = product_select, \
                               r_val = region_select, \
                               d_val = Date_slider,\
                               m_val = metric_select), code="""

    var all_data          = backup.data;
    var metric            = m_val.value
    console.log(m_val)

    var all_dates         = all_data['Date'];
    var all_metric        = all_data[metric];
    var all_prods         = all_data['Product'];
    var all_regions       = all_data['Region'];

    var filtered_dates      = [];
    var filtered_metric     = [];
    var filtered_products   = [];
    var filtered_regions    = [];

    var selected_prod     = p_val.value;
    var selected_reg      = r_val.value;
    var start_date        = d_val.value[0];
    var end_date          = d_val.value[1];

    for (var i = 0; i < all_dates.length; i++) {
        if ((all_prods[i] == selected_prod) && (all_regions[i] == selected_reg) && all_dates[i] >= start_date && all_dates[i] <= end_date) {
            filtered_dates.push(all_dates[i]);
            filtered_metric.push(all_metric[i]);
            filtered_products.push(all_prods[i])
            filtered_regions.push(all_regions[i])
        }
    }
    source.data['Date']      = filtered_dates;
    source.data['metric']    = filtered_metric;
    source.data['Product']   = filtered_products;
    source.data['Region']    = filtered_regions;

    source.change.emit();
""")

# # Create the updates for the JavaScript widgets
product_select.js_on_change('value', callback)
region_select.js_on_change('value', callback)
Date_slider.js_on_change('value', callback)
metric_select.js_on_change('value', callback)

# Create layout with graph and dropdowns
controls = column(product_select, region_select, Date_slider, metric_select)
layout   = row(controls, p)

# Show the plot
show(layout)
#output_file("Bokeh Plot.html") #To download the html file, click here


########################################################################################
#################### Unemployment Visualization Line Plot ##############################
########################################################################################

#Import the unemployment data and county codes excel sheet
unemployment_data = pd.read_csv("all_data_unemployment_retry_cleaned.csv")
county_data = pd.read_excel("County_Codes.xlsx", sheet_name = "States")

#Replace state codes with state abbreviations and type numbers with actual types
county_dict = county_data.set_index('Code').to_dict()['Abbreviation']
use_dictionary = use_dict = {3: "Unemployment", 6: "Labor Force Participation"}
unemployment_data['Type'] = unemployment_data['Type'].replace(use_dictionary)
unemployment_data['County']  = unemployment_data['County'].replace(county_dict)

#Ensure values are sorted properly
unemployment_data['Date']= pd.to_datetime(unemployment_data['Date'])
unemployment_data = unemployment_data.sort_values("County")
unemployment_data = unemployment_data.sort_values("Date")

#Initialize usable unemployment data starting in 2005
init_unemp_data = unemployment_data[unemployment_data['Year'] >= 2005]

#Changable Column Data Source
source = ColumnDataSource(data = dict(
        Date       = init_unemp_data ['Date'].values,
        Rate       = init_unemp_data ['Value'].values,
        Type       = init_unemp_data ['Type'].values,
        State      = init_unemp_data ['County'].values,
  ))

#Reference Column Data Source
backup = ColumnDataSource(data = dict(
        Date        = init_unemp_data ['Date'].values,
        Rate        = init_unemp_data ['Value'].values,
        Type        = init_unemp_data ['Type'].values,
        State       = init_unemp_data ['County'].values
  ))

#Create the figure
p = figure(x_axis_type = "datetime", x_axis_label="Date", y_axis_label="Value", \
           width = 800, height = 300)

#Add line to the figure
p.line('Date', 'Rate', source=source, line_width = 3)

#Create a dropdown for the type of statistic (Unemployment or Labor Force Participation)
type_select = Select(title="Select a Statistic:", \
                        value="Unemployment Rate", \
                        options=list(init_unemp_data['Type'].unique()))

#Create a data slider starting in 2005
Date_slider_2 = DateRangeSlider(value=(date(2005, 1, 1), date(2023, 10, 1)),
                                    start=date(2004, 1, 1), end=date(2023, 10, 1))

#Create a dropdown menu for the states in the US
State_select = Select(title = "Select a State:",\
                      value = "AL",\
                      options = list(init_unemp_data['County'].unique()))

#JavaScript code to update the dashboard dynamically.
callback2 = CustomJS(args=dict(source=source, \
                               backup = backup, \
                               t_val = type_select,\
                               d_val = Date_slider_2, \
                               s_val = State_select), code="""

    var all_data          = backup.data;

    var all_dates         = all_data['Date'];
    var all_rates         = all_data['Rate'];
    var all_types         = all_data['Type'];
    var all_counties      = all_data['State'];

    var filtered_dates      = [];
    var filtered_rates      = [];
    var filtered_types      = [];
    var filtered_counties   = [];

    var selected_type     = t_val.value;
    var start_date        = d_val.value[0];
    var end_date          = d_val.value[1];
    var selected_state    = s_val.value;
    console.log(selected_type);
    console.log(selected_state);

    for (var i = 0; i < all_dates.length; i++) {
        if ((all_types[i] == selected_type) && (all_dates[i] >= start_date) && (all_dates[i] <= end_date) && (all_counties[i] == selected_state)) {
            filtered_dates.push(all_dates[i]);
            filtered_rates.push(all_rates[i]);
            filtered_types.push(all_types[i]);
            filtered_counties.push(all_counties[i]);
        }
    }
    source.data['Date']      = filtered_dates;
    source.data['Rate']      = filtered_rates;
    source.data['Type']      = filtered_types;
    source.data['State']    = filtered_counties;

    source.change.emit();
""")

# # Create the dropdown updating code
type_select.js_on_change('value', callback2)
Date_slider_2.js_on_change('value', callback2)
State_select.js_on_change('value', callback2)

#Format the layout of the page
controls = column(type_select, Date_slider_2, State_select)
layout   = row(controls, p)

# Show plot
show(layout)
#output_file("Bokeh Plot.html") #For exporting html

########################################################################################
#################### Unemployment Visualization Map ####################################
########################################################################################

#Import the US states data set from Bokeh and use it to get latitude and longitude
#information for use in the heat maps
us_states_df = pd.DataFrame(us_states).T
us_states_df = us_states_df[~us_states_df["name"].isin(['Alaska', "Hawaii"])]
us_states_df["lons"] = us_states_df.lons.values.tolist()
us_states_df["lats"] = us_states_df.lats.values.tolist()
us_states_df = us_states_df.reset_index()

#Initialize a list for figures
figures = {}

#Loop through the 12 months
for i in range(1,13):
  
  # Create a data set for a given year (changed manually) and month (changed by the for loop)
  unemp_map_data = init_unemp_data[(init_unemp_data['Year'] == 2005) & (init_unemp_data['Month'] == i) 
                               & (init_unemp_data['Type'] == "Unemployment")]
  unemp_map_data = unemp_map_data.rename(columns={"Value": "Value_" + str(i)})
  
  #Merge the new unemployment data with the latitude and longitude data
  us_states_df = us_states_df.merge(unemp_map_data[["County", "Value_"+ str(i)]], how="left", left_on="index", right_on="County")
  
  #Create the figure
  fig = figure(width = 1100, height = 550,
             title="United States Unemployment Rates in 2005",
             x_axis_location=None, y_axis_location=None,
             tooltips=[
                        ("Name", "@name"), ("Unemployment", "@Value_"+str(i)), ("(Long, Lat)", "($x, $y)")
                      ])
  #Ensure we have no grid lines
  fig.grid.grid_line_color = None

  #Add color to the visualization
  fig.patches("lons", "lats", source=us_states_df,
            fill_color={'field': 'Value_'+str(i), 'transform': LogColorMapper(palette=YlGnBu[::-1])},
            fill_alpha=0.7, line_color="black", line_width=0.5)

  # Define a key for the colors
  cmap = LinearColorMapper(palette=YlGnBu[::-1], low=min(unemp_map_data['Value_' + str(i)].tolist()), high=max(unemp_map_data['Value_' + str(i)].tolist()))
  cbar = ColorBar(color_mapper=cmap)
  
  # Make the layout and add it to the list of figures
  fig.add_layout(cbar, 'left')
  figures[i] = fig

# Create each of the tabs in the visualization (based on months)
tab1 = TabPanel(child = figures[1], title = "January")
tab2 = TabPanel(child = figures[2], title = "February")
tab3 = TabPanel(child = figures[3], title = "March")
tab4 = TabPanel(child = figures[4], title = "April")
tab5 = TabPanel(child = figures[5], title = "May")
tab6 = TabPanel(child = figures[6], title = "June")
tab7 = TabPanel(child = figures[7], title = "July")
tab8 = TabPanel(child = figures[8], title = "August")
tab9 = TabPanel(child = figures[9], title = "September")
tab10 = TabPanel(child = figures[10], title = "October")
tab11 = TabPanel(child = figures[11], title = "November")
tab12 = TabPanel(child = figures[12], title = "December")

#Display all of the tabs
show(Tabs(tabs=[tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10,tab11,tab12]))
#output_file("Bokeh_Unemployment_2007.html") #For exporting files

########################################################################################
#################### Employment Visualization Line Plot ################################
########################################################################################

# Import the employment data and the list of county codes
employment_data = pd.read_csv("all_data_employment_retry_cleaned.csv")
county_data = pd.read_excel("County_Codes.xlsx", sheet_name = "States")

# Create dictionaries and replace selected values in the data set.
county_dict = county_data.set_index('Code').to_dict()['Abbreviation']
industry_dict = {1011: "Natural Resources and Mining",
                  1012: "Construction",
                  1013: "Manufacturing",
                  1021: "Trade, Transportation, and Utilities",
                  1022: "Information",
                  1023: "Financial Activities",
                  1024: "Professional and Business Services",
                  1025: "Education and Health Services",
                  1026: "Leisure and Hospitality",
                  1027: "Other Services",
                  1028: "Public Administration",
                  1029: "Unclassified"}
type_dict = {105: 'Employment', 405: 'Weekly Wage'}
employment_data['Type'] = employment_data['Type'].replace(type_dict)
employment_data['County']  = employment_data['County'].replace(county_dict)
employment_data['Industry']  = employment_data['Industry'].replace(industry_dict)

#Make the date and sort the values
employment_data['Date']= pd.to_datetime(employment_data['Date'])
employment_data = employment_data.sort_values("County")
employment_data = employment_data.sort_values("Date")

#Initialize usable employment data starting in 2005
init_emp_data = employment_data[employment_data['Year'] >= 2005]

# Changable Column Data Source
source = ColumnDataSource(data = dict(
        Date       = init_emp_data ['Date'].values,
        Rate       = init_emp_data ['Value'].values,
        Type       = init_emp_data ['Type'].values,
        State      = init_emp_data ['County'].values,
        Industry   = init_emp_data ['Industry'].values
  ))

#Reference Column Data Source
backup = ColumnDataSource(data = dict(
        Date        = init_emp_data ['Date'].values,
        Rate        = init_emp_data ['Value'].values,
        Type        = init_emp_data ['Type'].values,
        State       = init_emp_data ['County'].values,
        Industry    = init_emp_data ['Industry'].values
  ))

# Create the figure itself
p = figure(x_axis_type = "datetime", x_axis_label="Date", y_axis_label="Value", \
           width = 1200, height = 550)

# Make the line on the plot
p.line('Date', 'Rate', source=source, line_width = 3)

#Make a dropdown menu for the type of data (Employment and Weekly Wage)
type_select_2 = Select(title="Select a Statistic:", \
                        value="Employment", \
                        options=list(init_emp_data['Type'].unique()))

# Make a date slider starting in 2005
Date_slider_3 = DateRangeSlider(value=(date(2005, 1, 1), date(2023, 10, 1)),
                                    start=date(2005, 1, 1), end=date(2005, 10, 1))

# Make a state dropdown menu
State_select_2 = Select(title = "Select a State:",\
                      value = "AL",\
                      options = list(init_emp_data['County'].unique()))

# Make an industry dropdown menu
Industry_select = Select(title = "Select an Industry:",\
                         value = "Natural Resources and Mining",\
                         options = list(init_emp_data['Industry'].unique()))

#JavaScript for dynamically updating the dashboard
callback3 = CustomJS(args=dict(source=source, \
                               backup = backup, \
                               t_val = type_select_2,\
                               d_val = Date_slider_3, \
                               s_val = State_select_2,\
                               i_val = Industry_select), code="""

    var all_data          = backup.data;

    var all_dates         = all_data['Date'];
    var all_rates         = all_data['Rate'];
    var all_types         = all_data['Type'];
    var all_counties      = all_data['State'];
    var all_industries    = all_data['Industry'];

    var filtered_dates      = [];
    var filtered_rates      = [];
    var filtered_types      = [];
    var filtered_counties   = [];
    var filtered_industries = [];

    var selected_type     = t_val.value;
    var start_date        = d_val.value[0];
    var end_date          = d_val.value[1];
    var selected_state    = s_val.value;
    var selected_industry = i_val.value;
    console.log(selected_type);
    console.log(selected_state);

    for (var i = 0; i < all_dates.length; i++) {
        if ((all_types[i] == selected_type) && (all_dates[i] >= start_date) && (all_dates[i] <= end_date) && 
            (all_counties[i] == selected_state) && (all_industries[i] == selected_industry)) {
            filtered_dates.push(all_dates[i]);
            filtered_rates.push(all_rates[i]);
            filtered_types.push(all_types[i]);
            filtered_counties.push(all_counties[i]);
            filtered_industries.push(all_industries[i]);
        }
    }
    source.data['Date']      = filtered_dates;
    source.data['Rate']      = filtered_rates;
    source.data['Type']      = filtered_types;
    source.data['State']     = filtered_counties;
    source.data['Industry']  = filtered_industries;

    source.change.emit();
""")

# Connect the JavaScript code to the widgets
type_select_2.js_on_change('value', callback3)
Date_slider_3.js_on_change('value', callback3)
State_select_2.js_on_change('value', callback3)
Industry_select.js_on_change('value', callback3)

#Create the layout for the dashboard
controls = column(type_select_2, Date_slider_3, State_select_2, Industry_select)
layout   = row(controls, p)

# Show the plot
show(layout)
#output_file("Bokeh Plot.html")


########################################################################################
#################### Employment Visualization Map ######################################
########################################################################################

#Import the US states data set from Bokeh and use it to get latitude and longitude
#information for use in the heat maps
us_states_df = pd.DataFrame(us_states).T
us_states_df = us_states_df[~us_states_df["name"].isin(['Alaska', "Hawaii"])]
us_states_df["lons"] = us_states_df.lons.values.tolist()
us_states_df["lats"] = us_states_df.lats.values.tolist()
us_states_df = us_states_df.reset_index()

#Initialize a list for figures
figures = {}

# Replace the values for the industries for easier display 
industry_list = ["Resources_Mining", "Construction", "Manufacturing", "Trade_Transportation_Utilities",
                 "Information", "Financial_Activities", "Professional_Business_Services", "Education_Health_Services",
                 "Leisure_Hospitality", "Others"]
new_industry_dict = {"Natural Resources and Mining": "Resources_Mining",
                  "Construction": "Construction",
                  "Manufacturing": "Manufacturing",
                  "Trade, Transportation, and Utilities": "Trade_Transportation_Utilities",
                  "Information": "Information",
                  "Financial Activities": "Financial_Activities",
                  "Professional and Business Services": "Professional_Business_Services",
                  "Education and Health Services": "Education_Health_Services",
                  "Leisure and Hospitality": "Leisure_Hospitality",
                   "Other Services": "Others",
                  }
init_emp_data["Industry"] = init_emp_data["Industry"].replace(new_industry_dict)
init_emp_data["Value"] = init_emp_data["Value"].replace(to_replace = '-', value = np.nan)

# Loop through the industries
count = 0
for i in industry_list:
  count+=1
  
  # Create a data set for a given year, month, (changed manually) and industry (changed by the for loop)
  emp_map_data = init_emp_data[(init_emp_data['Year'] == 2005) & (init_emp_data['Period'] == 1) 
                            & (init_emp_data['Type'] == "Employment") & (init_emp_data['Industry'] == i)]
  emp_map_data = emp_map_data.rename(columns={"Value": "Value_"+str(count)})
  emp_map_data["Value_"+str(count)] = emp_map_data["Value_"+str(count)].astype(float)
  
  # Merge the employment data with the map data
  us_states_df = us_states_df.merge(emp_map_data[["County", "Value_"+str(count)]], how="left", left_on="index", right_on="County")
  
  # Create the employment map figure
  fig_2 = figure(width = 1100, height = 550,
             title="United States Employment in " + i + " January 2005",
             x_axis_location=None, y_axis_location=None,
             tooltips=[
                        ("Name", "@name"), ("Number Employed", "@Value_"+str(count)), ("(Long, Lat)", "($x, $y)")
                      ])
  # Remove the grid lines
  fig_2.grid.grid_line_color = None
  
  #Add the color to the map
  fig_2.patches("lons", "lats", source=us_states_df,
            fill_color={'field': 'Value_'+str(count), 'transform': LogColorMapper(palette=YlGnBu[::-1])},
            fill_alpha=0.7, line_color="black", line_width=0.5)
  
  # Create a legend for the map colors
  cmap_2 = LinearColorMapper(palette=YlGnBu[::-1], low=min(us_states_df['Value_'+str(count)].tolist()), high=max(us_states_df['Value_'+str(count)].tolist()))
  cbar_2 = ColorBar(color_mapper=cmap_2)
  fig_2.add_layout(cbar_2, 'left')
  figures[i] = fig_2

# Create the tabs for the visualization
Tab1 = TabPanel(child = figures["Resources_Mining"], title = "Natural Resources/Mining")
Tab2 = TabPanel(child = figures["Construction"], title = "Construction")
Tab3 = TabPanel(child = figures["Manufacturing"], title = "Manufacturing")
Tab4 = TabPanel(child = figures["Trade_Transportation_Utilities"], title = "Trade/Transportation/Utilities")
Tab5 = TabPanel(child = figures["Information"], title = "Information")
Tab6 = TabPanel(child = figures["Financial_Activities"], title = "Financial Activities")
Tab7 = TabPanel(child = figures["Professional_Business_Services"], title = "Professional/Business Services")
Tab8 = TabPanel(child = figures["Education_Health_Services"], title = "Education/Health Services")
Tab9 = TabPanel(child = figures["Leisure_Hospitality"], title = "Leisure/Hospitality")
Tab10 = TabPanel(child = figures["Others"], title = "Other")

# Display all the visualizations using tab method
show(Tabs(tabs=[Tab1,Tab2,Tab3,Tab4,Tab5,Tab6,Tab7,Tab8,Tab9,Tab10]))
#output_file("Employment_2005.html") #For exporting to html

