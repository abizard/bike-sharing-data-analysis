import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import plotly.express as px

#For Main Viz Tab
def create_monthly_avg_rent_df(df):
    monthly_rent_df = df.resample(rule='M', on='dteday').agg({
        'cnt_day' : 'mean',
        'casual_day' : 'mean',
        'registered_day' : 'mean'
    })

    monthly_rent_df.index = monthly_rent_df.index.strftime('%Y-%m')
    monthly_rent_df = monthly_rent_df.reset_index()
    monthly_rent_df.rename(columns={
        'cnt_day':'total_rental',
        'casual_day' : 'casual_renter',
        'registered_day' : 'registered_renter'
    }, inplace=True)

    return monthly_rent_df

def create_seasonal_avg_rent_df(df):
    seasonal_rent_df = df.groupby('season_day').agg({
        'cnt_day' : 'mean',
        'casual_day' : 'mean',
        'registered_day' : 'mean'
    })
    seasonal_rent_df = seasonal_rent_df.reset_index()
    seasonal_rent_df.rename(columns={
        'cnt_day':'total_rental',
        'casual_day' : 'casual_renter',
        'registered_day' : 'registered_renter'
    }, inplace=True)

    return seasonal_rent_df

def create_hourly_avg_rent_df(df):
    hourly_rent_df = df.groupby('hr').agg({
        'cnt_day' : 'mean',
        'casual_day' : 'mean',
        'registered_day' : 'mean'
    })
    hourly_rent_df = hourly_rent_df.reset_index()
    hourly_rent_df.rename(columns={
        'cnt_day':'total_rental',
        'casual_day' : 'casual_renter',
        'registered_day' : 'registered_renter'
    }, inplace=True)

    return hourly_rent_df

#For More Viz Tab
def create_seasonal_avg_rent_no_date_df(df):
    seasonal_rent_no_date_df = df[['season_day', 'cnt_day']]
    seasonal_rent_no_date_df = seasonal_rent_no_date_df.groupby('season_day')['cnt_day'].mean()
    seasonal_rent_no_date_df = seasonal_rent_no_date_df.reset_index()
    return seasonal_rent_no_date_df

def create_weather_avg_rent_no_date_df(df):
    weather_rent_no_date_df = df[['weathersit_day', 'cnt_day']]
    weather_rent_no_date_df = weather_rent_no_date_df.groupby('weathersit_day')['cnt_day'].mean()
    weather_rent_no_date_df = weather_rent_no_date_df.reset_index()
    return weather_rent_no_date_df

def create_hourly_rent_by_season_df(df, season):
    hourly_rent_by_season_df = df[['season_hour', 'hr', 'cnt_hour']]
    hourly_rent_by_season_df = hourly_rent_by_season_df[hourly_rent_by_season_df['season_hour'] == season].groupby(['season_hour','hr'])['cnt_hour'].mean()
    hourly_rent_by_season_df = hourly_rent_by_season_df.reset_index()
    return hourly_rent_by_season_df

bike_df = pd.read_csv('https://raw.githubusercontent.com/abizard/bike-sharing-data-analysis/main/dashboard/bike_df.csv')
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])

min_date = bike_df['dteday'].min()
max_date = bike_df['dteday'].max()

with st.sidebar:
    st.header('Bike Sharing Data Analysis')
    st.image('https://mir-s3-cdn-cf.behance.net/project_modules/disp/710b4d66481317.5b17972b11d62.jpg')

    start_date, end_date = st.date_input(
        label='Pilih rentang waktu :', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bike_df[(bike_df['dteday'] >= str(start_date)) & 
                (bike_df['dteday'] <= str(end_date))]

monthly_rent_df = create_monthly_avg_rent_df(main_df)
seasonal_rent_df = create_seasonal_avg_rent_df(main_df)
hourly_rent_df = create_hourly_avg_rent_df(main_df)
seasonal_rent_no_date_df = create_seasonal_avg_rent_no_date_df(bike_df)
weather_rent_no_date_df = create_weather_avg_rent_no_date_df(bike_df)

st.header('Bike Sharing Dashboard 🚲:sparkles:')
st.markdown(
    """
    - **Nama:** Abizard Hashfi Darmawan
    - **Email:** abizard.03@gmail.com
    - **ID Dicoding:** abizardhashfid
    """
)
st.subheader('Overall Renters (Day)')

col1, col2, col3 = st.columns(3)
with col1:
    cnt_rent = main_df['cnt_day'].sum()
    formatted_cnt_rent = '{:,.0f}'.format(cnt_rent).replace(',', '.')
    st.metric('Rental Amount ', value=formatted_cnt_rent)

with col2:
    casual_renter = main_df['casual_day'].sum()
    formatted_casual_renter = '{:,.0f}'.format(casual_renter).replace(',', '.')
    st.metric('Total Casual Renters ', value=formatted_casual_renter)

with col3:
    registered_renter = main_df['registered_day'].sum()
    formatted_registered_renter = '{:,.0f}'.format(registered_renter).replace(',', '.')
    st.metric('Total Registered Renters ', value=formatted_registered_renter)

tab1, tab2 = st.tabs(['Main Viz', 'More Viz'])

with tab1:
    st.subheader('Main Visualization 📊')
    st.write('***\*Gunakan date input pada sidebar untuk mengatur visualisasi***')
    monthly_rent_chart = px.line(
       monthly_rent_df, 
       x='dteday', 
       y=['total_rental', 'casual_renter', 'registered_renter'], 
       color_discrete_sequence=px.colors.qualitative.G10,
       title='Average Monthly Bike Rental',
       markers=True
    )
    st.plotly_chart(monthly_rent_chart.update_layout(xaxis_title='Date', yaxis_title='Rental Amount (Avg)'))

    seasonal_rent_chart = px.bar(
        seasonal_rent_df,
        x='season_day',
        y=["casual_renter", "registered_renter"],
        title='Average Bike Rental by Season (Based on Date)',
        color_discrete_sequence=px.colors.qualitative.G10
    )
    st.plotly_chart(seasonal_rent_chart.update_layout(xaxis_title='Season', yaxis_title='Rental Amount (Avg)'))

    hourly_rent_chart = px.bar(
        hourly_rent_df,
        x='hr',
        y=["casual_renter", "registered_renter"],
        title='Average Bike Rental by Hour (Based on Date)',
        color_discrete_sequence=px.colors.qualitative.G10
    )
    st.plotly_chart(hourly_rent_chart.update_layout(xaxis_title='Hour', yaxis_title='Rental Amount (Avg)'))

with tab2:
    st.subheader('More Visualization 📊')
    seasonal_rent_no_date_chart = px.bar(
        seasonal_rent_no_date_df,
        x='season_day',
        y='cnt_day',
        color='season_day',
        title='Average of Bike Rental based on Season'
    )
    st.plotly_chart(seasonal_rent_no_date_chart.update_layout(xaxis_title='Season', yaxis_title='Mean Count'))

    weather_rent_no_date_chart = px.bar(
        weather_rent_no_date_df,
        x='weathersit_day',
        y='cnt_day',
        color='weathersit_day',
        title='Average of Bike Rental based on Weather'
    )
    st.plotly_chart(weather_rent_no_date_chart.update_layout(xaxis_title='Weathersit', yaxis_title='Mean Count'))

    season = st.selectbox(
        label="Pilih jenis musim:",
        options=('Fall', 'Spring', 'Summer', 'Winter')
    )

    color_palette = {
        'Fall': px.colors.qualitative.Plotly[2],
        'Spring': px.colors.qualitative.Plotly[3],
        'Summer': px.colors.qualitative.Plotly[1],
        'Winter': px.colors.qualitative.Plotly[0]
    }

    color = color_palette.get(season, 'blue')

    hourly_rent_by_season_df = create_hourly_rent_by_season_df(bike_df, season)
    hourly_rent_by_season_chart = px.bar(
        hourly_rent_by_season_df,
        x='hr',
        y='cnt_hour',
        color_discrete_sequence=[color],
        title=f'Average Bike Rental Count per Hour by Season ({season})'
    )
    st.plotly_chart(hourly_rent_by_season_chart.update_layout(xaxis_title='Hour', yaxis_title='Mean Count'))
st.caption('Copyright © 2023. Made with ❤️')