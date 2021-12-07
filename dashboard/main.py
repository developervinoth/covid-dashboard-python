import pandas as pd
import plotly.graph_objects as go
import streamlit as stl
import plotly.express as px
# dataset for postive cases from github
global_data = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

# dataset for deaths from github
death_data = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

# creating dataframe from github source file
positive_cases = pd.read_csv(global_data)
deaths = pd.read_csv(death_data)

# Transposing dataframe based Column(Date) ----> Row(date)
df_cases = positive_cases.melt(id_vars=['Country/Region', 'Province/State',
                                        'Lat', 'Long'], var_name='Date', value_name='Cases')

df_deaths = deaths.melt(id_vars=['Country/Region', 'Province/State',
                                 'Lat', 'Long'], var_name='Date', value_name='Cases')

# Date columns datatime changed to DateTime
df_cases['Date'] = pd.to_datetime(df_cases['Date'])
df_deaths['Date'] = pd.to_datetime(df_cases['Date'])

# removing unwanted rows
df_cases.drop(columns=['Province/State', 'Lat', 'Long'], inplace=True)
df_deaths.drop(columns=['Province/State', 'Lat', 'Long'], inplace=True)

#Tabs
tabs = ['Cases', 'Deaths', 'Vaccinations', 'Tests']

# Defining Columns 
col1, col2 = stl.columns(2)

# Selectbox for Tab Selection
tab_select = stl.sidebar.radio('Select Tab', tabs)
country_list =  list(df_cases['Country/Region'].unique())
print('Starting Length: ', len(country_list))
country_list.remove('India')
print('Removing India: ', len(country_list))
country_list.insert(0, 'India')
print('Adding India', len(country_list))
# Streamlit selectbox for country selection
country_select = stl.sidebar.selectbox(
    'Select Country',country_list)
temp_value = 0
def dailyCal(currentRow):
    global temp_value
    todayDeath = currentRow-temp_value
    temp_value = currentRow
    return int(todayDeath)

#Cases Page
if tab_select == tabs[0]:
    # Confirmed Case by Country Selection
    col1.title('Total Cases')
    col1.subheader(str((df_cases[df_cases['Country/Region'] ==
              country_select].tail(1).Cases.values[0])/1000) + 'K')
              
    # Currently Active Cases
    col2.title('Active Cases')
    col2.subheader((df_cases[df_cases['Country/Region'] == country_select][-2:-1].Cases.values[0]) -
              (df_cases[df_cases['Country/Region'] == country_select][-3:-2].Cases.values[0]))
    df_cases['Daily_Cases'] = df_cases[df_cases['Country/Region'] == country_select]['Cases'].apply(lambda x: dailyCal(x))
    temp_value = 0
    
    country_df_cases = df_cases[df_cases['Country/Region'] == country_select]
    fig = px.line(data_frame= country_df_cases, x= 'Date', y='Daily_Cases')
    fig.update_xaxes(showgrid=False, tickformat='%b %Y')
    fig.update_yaxes(showgrid=False)
    fig.update_layout(hovermode="x unified", hoverlabel=dict(
         bgcolor="white",
         font_size=9,
         font_family="Arial"
     ))
    stl.plotly_chart(fig)
    
    print(df_cases)


# Death Page
if tab_select == tabs[1]:
        #Total Deaths
    stl.title('Total Deaths')
    deathInNumber = df_deaths[df_deaths['Country/Region'] == country_select].tail(1).Cases.values[0]
    
    if deathInNumber > 100000:
        stl.subheader(str(round(((df_deaths[df_deaths['Country/Region'] ==
              country_select].tail(1).Cases.values[0])/100000),2)) + 'L')
    if deathInNumber < 100000:
            stl.subheader(str((((df_deaths[df_deaths['Country/Region'] ==
              country_select].tail(1).Cases.values[0])))))


    
    df_deaths_duplicate = df_deaths.copy()

    
    country_df_deaths = df_deaths_duplicate[df_deaths_duplicate['Country/Region'] == country_select]

    country_df_deaths['Daily_Deaths'] = country_df_deaths[country_df_deaths['Country/Region'] == country_select]['Cases'].apply(lambda x: dailyCal(x))
    temp_value = 0


    fig = px.line(data_frame=country_df_deaths, x='Date', y='Daily_Deaths')

    fig.update_xaxes(showgrid=False, tickformat='%b %Y')
    fig.update_yaxes(showgrid=False)
    fig.update_layout(hovermode="x unified", hoverlabel=dict(
        bgcolor="white",
        font_size=9,
        font_family="Arial"
    ))
    
    
    
    stl.plotly_chart(fig)
    