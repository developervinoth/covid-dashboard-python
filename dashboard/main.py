import pandas as pd
import streamlit as stl

global_data = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
raw_df = pd.read_csv(global_data)

df = raw_df.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long'] ,var_name= 'Date', value_name='Cases')

df.drop(columns=['Province/State','Lat','Long'], inplace=True)
country_select = stl.selectbox('Select Country', list(df['Country/Region'].unique()))

stl.table(df[df['Country/Region'] == country_select])

print(df)

