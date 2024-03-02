import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import plotly.express as px

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
    title='Average Bike Rental by Season',
    color_discrete_sequence=px.colors.qualitative.G10
)
st.plotly_chart(seasonal_rent_chart.update_layout(xaxis_title='Season', yaxis_title='Rental Amount (Avg)'))

hourly_rent_chart = px.bar(
    hourly_rent_df,
    x='hr',
    y=["casual_renter", "registered_renter"],
    title='Average Bike Rental by Hour',
    color_discrete_sequence=px.colors.qualitative.G10
)
st.plotly_chart(hourly_rent_chart.update_layout(xaxis_title='Hour', yaxis_title='Rental Amount (Avg)'))
st.caption('Copyright © 2023. Made with ❤️')