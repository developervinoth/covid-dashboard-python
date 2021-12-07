import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as stl
import plotly.express as px
#dataset from github
global_data = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

#creating dataset from github source file
raw_df = pd.read_csv(global_data)

#Transposing dataframe based Column(Date) ----> Row(date)
df = raw_df.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long'] ,var_name= 'Date', value_name='Cases')
df['Date'] = pd.to_datetime(df['Date'])
#removing unwanted rows
df.drop(columns=['Province/State','Lat','Long'], inplace=True)

#Streamlit selectbox for country selection
country_select = stl.sidebar.selectbox('Select Country', list(df['Country/Region'].unique()))


#table of selected country
#stl.table(df[df['Country/Region'] == country_select])


country_df = df[df['Country/Region'] == country_select]

fig = px.line(data_frame=country_df,x = 'Date', y='Cases')

fig.update_xaxes(showgrid=False, tickformat = '%b %Y')
fig.update_yaxes(showgrid=False )
fig.update_layout(hovermode="x unified",hoverlabel=dict(
        bgcolor="white",
        font_size=9,
        font_family="Arial",
    ))
stl.plotly_chart(fig)
print(df)

