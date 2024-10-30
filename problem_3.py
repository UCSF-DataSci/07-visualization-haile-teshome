import streamlit as st
import pandas as pd
import plotly.express as px

#Set the page layout to wide for full width page
st.set_page_config(layout="wide") 

#List of countries to include in the dashboard
countries = ['abw', 'usa', 'chn', 'ind', 'bra', 'can', 'mex', 'deu', 'fra', 'jpn']

#Data directory path
data_dir = '/Users/hteshome/Desktop/Training/Pytools_Class/07-visualization-haile-teshome/ddf--datapoints--population--by--country--age--gender--year'

#Function to load data for selected countries
@st.cache_data
def load_data(selected_countries):
    dfs = []
    for country in selected_countries:
        df_country = pd.read_csv(f'{data_dir}/ddf--datapoints--population--by--country-{country}--age--gender--year.csv')
        df_country['country'] = country
        dfs.append(df_country)
    return pd.concat(dfs)

#Interactive sidebar for parameter selection
st.sidebar.title('Interactive Population Dashboard')
st.sidebar.subheader('Select countries')
selected_countries = st.sidebar.multiselect('Choose countries', countries, default=['usa', 'chn', 'ind'])

#Load the combined data for the selected countries
df_combined = load_data(selected_countries)

#Sidebar filters for select parameters
year_range = st.sidebar.slider('Select Year Range', min_value=int(df_combined['year'].min()), 
                               max_value=int(df_combined['year'].max()), value=(2000, 2020))

age_range = st.sidebar.slider('Select Age Range', min_value=int(df_combined['age'].min()), 
                              max_value=int(df_combined['age'].max()), value=(0, 80))

#Filter the data for the selected year range and age group
df_filtered = df_combined[(df_combined['year'] >= year_range[0]) & (df_combined['year'] <= year_range[1])]
df_filtered = df_filtered[(df_filtered['age'] >= age_range[0]) & (df_filtered['age'] <= age_range[1])]

#Space formatting
st.markdown("<br>", unsafe_allow_html=True)

#Create a header for the dashboard
st.title(f'Population Distribution from {year_range[0]} to {year_range[1]}')

st.markdown("<br><br>", unsafe_allow_html=True)

#Population graph
st.subheader('Population Trends Over Time')
df_line_chart = df_filtered.groupby(['year', 'country'])['population'].sum().reset_index()
fig = px.line(df_line_chart, x='year', y='population', color='country', 
              title='Total Population by Country Over Time',
              labels={'population': 'Total Population', 'year': 'Year'},
              markers=True)
st.plotly_chart(fig, use_container_width=True, height=500)  # Full width chart

#Display key population statistics
st.subheader('Key Population Statistics')
key_stats = df_filtered.groupby('country')['population'].agg(['mean', 'sum', 'max', 'min', 'median', 'std', 'var']).reset_index()
st.table(key_stats)

st.markdown("<br><br>", unsafe_allow_html=True)

st.subheader('Population Distribution by Age and Gender')

col3, col4 = st.columns([1, 1])  

#Population Distribution by Age Group
with col3:
    df_age_group_plot = df_filtered.groupby('age')['population'].sum().reset_index()
    fig2 = px.bar(df_age_group_plot, x='age', y='population', title='Population by Age Group',
                  labels={'age': 'Age', 'population': 'Population'}, 
                  color='age', color_continuous_scale='Blues')
    st.plotly_chart(fig2, use_container_width=True, height=500)

#Population Distribution by Gender
with col4:
    df_gender_plot = df_filtered.groupby('gender')['population'].sum().reset_index()
    df_gender_plot['gender'] = df_gender_plot['gender'].map({1: 'Male', 2: 'Female'})  # Map gender values to labels
    fig3 = px.bar(df_gender_plot, x='population', y='gender', orientation='h', 
                  title='Population Distribution by Gender', 
                  labels={'population': 'Population', 'gender': 'Gender'}, 
                  color='gender', color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig3, use_container_width=True, height=500)

st.markdown("<br><br>", unsafe_allow_html=True)

#Add a section for filtered data at the bottom
st.subheader('Filtered Population Data')
st.dataframe(df_filtered[['country', 'year', 'age', 'gender', 'population']])
