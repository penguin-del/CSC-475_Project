# -*- coding: utf-8 -*-
"""
@name: visualization.py
@desc: this file cleans the downloaded data from import.py
@date: October 19th, 2023
@author: Joshua Hutson
"""

from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure, show
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as counties
from bokeh.io import output_file
import pandas as pd
from bokeh.models import CustomJS, Dropdown

Inflation = pd.read_csv("all_data_inflation_cleaned.csv")
Inflation = Inflation.drop('Unnamed: 0', axis=1)
# create a new plot (with a title) using figure
p = figure(width=400, height=400, title="My Line Plot")
p = figure(x_axis_type="datetime", title="CPI Over Time", height=350, width=800)
# add a line renderer
Inflation['Year'] = Inflation['Year'].astype(int)
Inflation = Inflation.sort_values('Year')
p.line(Inflation['Year'].astype(int), Inflation['CPI value'], line_width=2)

show(p) # show the results



menu = [("Cereals/Wheats", "Cereals/Wheats"), ("Meat", "Meat"), ("Fruit and Vegetable", "Fruit and Vegetable"), 
        ("Non-alcoholic Beverages", "Non-alcoholic Beverages"), ("Dairy", "Dairy"), ("Housing", "Housing"),
        ("Food Away From Home", "Food Away From Home"), ("Household Energy", "Household energy"), 
        ("Clothes/Apparel"), ("New cars", "New cars"), ("Used cars", "Used cars"), ("Gasoline", "Gasoline")]

dropdown = Dropdown(label="Dropdown button", button_type="warning", menu=menu)
dropdown.js_on_event("menu_item_click", CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"))

show(dropdown)

# for time : p = figure(x_axis_type = "datetime", title = "My title")
# Creating a map:
# from bokeh.plotting import figure
#from bokeh.models import WMTSTileSource

# web mercator coordinates
#USA = x_range,y_range = ((-13884029,-7453304), (2698291,6455972))

#p = figure(tools='pan, wheel_zoom', x_range=x_range, y_range=y_range, 
          # x_axis_type="mercator", y_axis_type="mercator")

#palette = tuple(reversed(palette))

#from datetime import date

#from bokeh.io import show
#from bokeh.models import CustomJS, DateRangeSlider


#date_range_slider = DateRangeSlider(value=(date(2016, 1, 1), date(2016, 12, 31)),
#                                    start=date(2015, 1, 1), end=date(2017, 12, 31))
#date_range_slider.js_on_change("value", CustomJS(code="""
 #   console.log('date_range_slider: value=' + this.value, this.toString())
#"""))

#show(date_range_slider)

# from bokeh.layouts import column 
# from bokeh.models import ColumnDataSource, Slider, CustomJS 
# from bokeh.plotting import figure, output_file, show 
# import numpy as np 
# from bokeh.io import reset_output, output_notebook

# reset_output()
# output_notebook()

# x = np.linspace(0, 10, 500) 
# y = np.sin(x) 
  
# source = ColumnDataSource(data=dict(x=x, y=y)) 
  
# # Create plots and widgets 
# plot = figure() 
  
# plot.line('x', 'y', source=source, line_width=3, line_alpha=0.5) 
  
# # Create Slider object 
# slider = Slider(start=0, end=6, value=2, 
#                 step=0.2, title='Number of points') 
  
# # Adding callback code 
# callback = CustomJS(args=dict(source=source, val=slider), 
#                     code=""" 
#     const data = source.data; 
#     const freq = val.value; 
#     const x = data['x']; 
#     const y = data['y']; 
#    for (var i = 0; i < x.length; i++) { 
#         y[i] = Math.sin(freq*x[i]); 
#     } 
#     source.change.emit(); 
# """) 
  
# slider.js_on_change('value', callback) 
  
# # Arrange plots and widgets in layouts 
# layout = column(slider, plot) 
  
# # output_file('exam.html') 
  
# show(layout) 

### Special Map Code (figure out what to do)
# counties = {
#     code: county for code, county in counties.items() 
# }

# county_xs = [county["lons"] for county in counties.values()]
# county_ys = [county["lats"] for county in counties.values()]

# county_names = [county['name'] for county in counties.values()]
# county_rates = [unemployment[county_id] for county_id in counties]
# color_mapper = LogColorMapper(palette=palette)

# data=dict(
#     x=county_xs,
#     y=county_ys,
#     name=county_names,
#     rate=county_rates,
# )

# TOOLS = "pan,wheel_zoom,reset,hover,save"

# p = figure(
#     title="Texas Unemployment, 2009", tools=TOOLS,
#     x_axis_location=None, y_axis_location=None,
#     tooltips=[
#         ("Name", "@name"), ("Unemployment rate", "@rate%"), ("(Long, Lat)", "($x, $y)"),
#     ])
# p.grid.grid_line_color = None
# p.hover.point_policy = "follow_mouse"

# p.patches('x', 'y', source=data,
#           fill_color={'field': 'rate', 'transform': color_mapper},
#           fill_alpha=0.7, line_color="white", line_width=0.5)

# output_file("plot.html")