import pandas as pd
import streamlit as stl


#dataset from github
global_data = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

#creating dataset from github source file
raw_df = pd.read_csv(global_data)

#Transposing dataframe based Column(Date) ----> Row(date)
df = raw_df.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long'] ,var_name= 'Date', value_name='Cases')

#removing unwanted rows
df.drop(columns=['Province/State','Lat','Long'], inplace=True)

#Streamlit selectbox for country selection
country_select = stl.selectbox('Select Country', list(df['Country/Region'].unique()))

#table of selected country
stl.table(df[df['Country/Region'] == country_select])

print(df)

