import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="COVID-19 Global Dashboard",
    page_icon="🦠",
    layout="wide"
)

# Title and introduction
st.title("COVID-19 Global Dashboard")
st.markdown("""
This dashboard visualizes COVID-19 data from around the world, showing trends in confirmed cases, 
deaths, and recoveries. Use the sidebar to navigate between different views and analyses.
""")

@st.cache_data
def load_data():
    # Load the data
    df = pd.read_csv('covid_19_data.csv', parse_dates=['ObservationDate'])
    df.rename(columns={'Country/Region': 'Country'}, inplace=True)
    df['Province/State'].fillna('Unknown', inplace=True)
    
    # Aggregate by country and date
    df = df.groupby(['Country', 'ObservationDate']).sum().reset_index()
    
    # Add continent mapping
    continent_mapping = {
        'Afghanistan': 'Asia', 'Albania': 'Europe', 'Algeria': 'Africa',
        'Andorra': 'Europe', 'Angola': 'Africa', 'Antigua and Barbuda': 'North America',
        'Argentina': 'South America', 'Armenia': 'Asia', 'Aruba': 'North America',
        'Australia': 'Oceania', 'Austria': 'Europe', 'Azerbaijan': 'Asia',
        'Bahamas': 'North America', 'Bahamas, The': 'North America', 'Bahrain': 'Asia',
        'Bangladesh': 'Asia', 'Barbados': 'North America', 'Belarus': 'Europe',
        'Belgium': 'Europe', 'Belize': 'North America', 'Benin': 'Africa',
        'Bhutan': 'Asia', 'Bolivia': 'South America', 'Bosnia and Herzegovina': 'Europe',
        'Botswana': 'Africa', 'Brazil': 'South America', 'Brunei': 'Asia',
        'Bulgaria': 'Europe', 'Burkina Faso': 'Africa', 'Burma': 'Asia',
        'Burundi': 'Africa', 'Cabo Verde': 'Africa', 'Cambodia': 'Asia',
        'Cameroon': 'Africa', 'Canada': 'North America', 'Cape Verde': 'Africa',
        'Cayman Islands': 'North America', 'Central African Republic': 'Africa',
        'Chad': 'Africa', 'Channel Islands': 'Europe', 'Chile': 'South America',
        'China': 'Asia', 'Colombia': 'South America', 'Comoros': 'Africa',
        'Congo (Brazzaville)': 'Africa', 'Congo (Kinshasa)': 'Africa',
        'Costa Rica': 'North America', 'Croatia': 'Europe', 'Cuba': 'North America',
        'Curacao': 'North America', 'Cyprus': 'Europe', 'Czech Republic': 'Europe',
        'Denmark': 'Europe', 'Diamond Princess': 'Others', 'Djibouti': 'Africa',
        'Dominica': 'North America', 'Dominican Republic': 'North America',
        'East Timor': 'Asia', 'Ecuador': 'South America', 'Egypt': 'Africa',
        'El Salvador': 'North America', 'Equatorial Guinea': 'Africa',
        'Eritrea': 'Africa', 'Estonia': 'Europe', 'Eswatini': 'Africa',
        'Ethiopia': 'Africa', 'Faroe Islands': 'Europe', 'Fiji': 'Oceania',
        'Finland': 'Europe', 'France': 'Europe', 'French Guiana': 'South America',
        'Gabon': 'Africa', 'Gambia': 'Africa', 'Gambia, The': 'Africa',
        'Georgia': 'Asia', 'Germany': 'Europe', 'Ghana': 'Africa',
        'Gibraltar': 'Europe', 'Greece': 'Europe', 'Greenland': 'North America',
        'Grenada': 'North America', 'Guadeloupe': 'North America', 'Guam': 'Oceania',
        'Guatemala': 'North America', 'Guernsey': 'Europe', 'Guinea': 'Africa',
        'Guinea-Bissau': 'Africa', 'Guyana': 'South America', 'Haiti': 'North America',
        'Holy See': 'Europe', 'Honduras': 'North America', 'Hong Kong': 'Asia',
        'Hungary': 'Europe', 'Iceland': 'Europe', 'India': 'Asia',
        'Indonesia': 'Asia', 'Iran': 'Asia', 'Iraq': 'Asia',
        'Ireland': 'Europe', 'Israel': 'Asia', 'Italy': 'Europe',
        'Ivory Coast': 'Africa', 'Jamaica': 'North America', 'Japan': 'Asia',
        'Jersey': 'Europe', 'Jordan': 'Asia', 'Kazakhstan': 'Asia',
        'Kenya': 'Africa', 'Kiribati': 'Oceania', 'Kosovo': 'Europe',
        'Kuwait': 'Asia', 'Kyrgyzstan': 'Asia', 'Laos': 'Asia',
        'Latvia': 'Europe', 'Lebanon': 'Asia', 'Lesotho': 'Africa',
        'Liberia': 'Africa', 'Libya': 'Africa', 'Liechtenstein': 'Europe',
        'Lithuania': 'Europe', 'Luxembourg': 'Europe', 'MS Zaandam': 'Others',
        'Macau': 'Asia', 'Madagascar': 'Africa', 'Mainland China': 'Asia',
        'Malawi': 'Africa', 'Malaysia': 'Asia', 'Maldives': 'Asia',
        'Mali': 'Africa', 'Malta': 'Europe', 'Marshall Islands': 'Oceania',
        'Martinique': 'North America', 'Mauritania': 'Africa', 'Mauritius': 'Africa',
        'Mayotte': 'Africa', 'Mexico': 'North America', 'Micronesia': 'Oceania',
        'Moldova': 'Europe', 'Monaco': 'Europe', 'Mongolia': 'Asia',
        'Montenegro': 'Europe', 'Morocco': 'Africa', 'Mozambique': 'Africa',
        'Namibia': 'Africa', 'Nepal': 'Asia', 'Netherlands': 'Europe',
        'New Zealand': 'Oceania', 'Nicaragua': 'North America', 'Niger': 'Africa',
        'Nigeria': 'Africa', 'North Ireland': 'Europe', 'North Macedonia': 'Europe',
        'Norway': 'Europe', 'Oman': 'Asia', 'Others': 'Others',
        'Pakistan': 'Asia', 'Palestine': 'Asia', 'Panama': 'North America',
        'Papua New Guinea': 'Oceania', 'Paraguay': 'South America', 'Peru': 'South America',
        'Philippines': 'Asia', 'Poland': 'Europe', 'Portugal': 'Europe',
        'Puerto Rico': 'North America', 'Qatar': 'Asia', 'Republic of Ireland': 'Europe',
        'Republic of the Congo': 'Africa', 'Reunion': 'Africa', 'Romania': 'Europe',
        'Russia': 'Europe', 'Rwanda': 'Africa', 'Saint Barthelemy': 'North America',
        'Saint Kitts and Nevis': 'North America', 'Saint Lucia': 'North America',
        'Saint Vincent and the Grenadines': 'North America', 'Samoa': 'Oceania',
        'San Marino': 'Europe', 'Sao Tome and Principe': 'Africa', 'Saudi Arabia': 'Asia',
        'Senegal': 'Africa', 'Serbia': 'Europe', 'Seychelles': 'Africa',
        'Sierra Leone': 'Africa', 'Singapore': 'Asia', 'Slovakia': 'Europe',
        'Slovenia': 'Europe', 'Solomon Islands': 'Oceania', 'Somalia': 'Africa',
        'South Africa': 'Africa', 'South Korea': 'Asia', 'South Sudan': 'Africa',
        'Spain': 'Europe', 'Sri Lanka': 'Asia', 'St. Martin': 'North America',
        "('St. Martin',)": 'North America', 'Sudan': 'Africa', 'Suriname': 'South America',
        'Sweden': 'Europe', 'Switzerland': 'Europe', 'Syria': 'Asia',
        'Taiwan': 'Asia', 'Tajikistan': 'Asia', 'Tanzania': 'Africa',
        'Thailand': 'Asia', 'The Bahamas': 'North America', 'The Gambia': 'Africa',
        'Timor-Leste': 'Asia', 'Togo': 'Africa', 'Trinidad and Tobago': 'North America',
        'Tunisia': 'Africa', 'Turkey': 'Asia', 'UK': 'Europe',
        'US': 'North America', 'Uganda': 'Africa', 'Ukraine': 'Europe',
        'United Arab Emirates': 'Asia', 'Uruguay': 'South America', 'Uzbekistan': 'Asia',
        'Vanuatu': 'Oceania', 'Vatican City': 'Europe', 'Venezuela': 'South America',
        'Vietnam': 'Asia', 'West Bank and Gaza': 'Asia', 'occupied Palestinian territory': 'Asia',
        'Yemen': 'Asia', 'Zambia': 'Africa', 'Zimbabwe': 'Africa'
    }
    
    df['Continent'] = df['Country'].map(continent_mapping)
    
    # Create global data summary
    global_data = df.groupby('ObservationDate').agg({
        'Confirmed': 'sum',
        'Deaths': 'sum',
        'Recovered': 'sum'
    }).reset_index()
    
    # Calculate daily increases
    global_data['Daily_Confirmed'] = global_data['Confirmed'].diff().fillna(0)
    global_data['Daily_Deaths'] = global_data['Deaths'].diff().fillna(0)
    global_data['Daily_Recovered'] = global_data['Recovered'].diff().fillna(0)
    
    # Get latest data for each country
    latest_date = df['ObservationDate'].max()
    latest_data = df[df['ObservationDate'] == latest_date]
    
    # Calculate mortality rate
    latest_data['Mortality_Rate'] = (latest_data['Deaths'] / latest_data['Confirmed'] * 100).round(2)
    
    # Create continent summary
    continent_data = df.groupby(['Continent', 'ObservationDate']).sum().reset_index()
    
    return df, global_data, latest_data, continent_data

# Create sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    ["Global Overview", "Country Analysis", "Continental Trends", "Mortality Analysis"]
)

# Load data
try:
    df, global_data, latest_data, continent_data = load_data()
    
    # Display a loading message while data loads
    data_load_state = st.text('Loading data...')
    data_load_state.text('Data loaded successfully!')
    
    # Global Overview page
    if page == "Global Overview":
        st.header("Global COVID-19 Overview")
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        latest_global = global_data.iloc[-1]
        
        col1.metric(
            "Total Confirmed Cases", 
            f"{int(latest_global['Confirmed']):,}", 
            f"+{int(latest_global['Daily_Confirmed']):,}"
        )
        
        col2.metric(
            "Total Deaths", 
            f"{int(latest_global['Deaths']):,}", 
            f"+{int(latest_global['Daily_Deaths']):,}"
        )
        
        col3.metric(
            "Total Recovered", 
            f"{int(latest_global['Recovered']):,}", 
            f"+{int(latest_global['Daily_Recovered']):,}"
        )
        
        # Global trend chart
        st.subheader("Global COVID-19 Trends")
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(
                x=global_data['ObservationDate'], 
                y=global_data['Confirmed'], 
                name='Total Cases',
                line=dict(color='blue')
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=global_data['ObservationDate'], 
                y=global_data['Deaths'], 
                name='Total Deaths',
                line=dict(color='red')
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=global_data['ObservationDate'], 
                y=global_data['Recovered'], 
                name='Total Recovered',
                line=dict(color='green')
            )
        )
        
        fig.update_layout(
            title='Global COVID-19 Trends',
            xaxis_title='Date',
            yaxis_title='Count',
            legend_title='Metric',
            hovermode='x unified',
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Daily cases chart
        st.subheader("Daily New Cases and Deaths")
        
        fig = px.area(
            global_data,
            x='ObservationDate',
            y='Daily_Confirmed',
            title='Daily New Cases'
        )
        
        fig.add_scatter(
            x=global_data['ObservationDate'], 
            y=global_data['Daily_Deaths'], 
            name='Daily Deaths', 
            line=dict(color='red')
        )
        
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Count',
            legend_title='Metric',
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Country Analysis page
    elif page == "Country Analysis":
        st.header("Country-level Analysis")
        
        # Country selection
        selected_country = st.selectbox(
            "Select a country to analyze",
            sorted(df['Country'].unique())
        )
        
        # Filter data for selected country
        country_data = df[df['Country'] == selected_country]
        
        # Display country metrics
        latest_country = country_data[country_data['ObservationDate'] == country_data['ObservationDate'].max()].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Total Cases", f"{int(latest_country['Confirmed']):,}")
        col2.metric("Total Deaths", f"{int(latest_country['Deaths']):,}")
        col3.metric("Mortality Rate", f"{(latest_country['Deaths'] / latest_country['Confirmed'] * 100):.2f}%")
        
        # Country trend chart
        st.subheader(f"COVID-19 Trends in {selected_country}")
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=country_data['ObservationDate'], 
                y=country_data['Confirmed'], 
                name='Confirmed Cases',
                line=dict(color='blue')
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=country_data['ObservationDate'], 
                y=country_data['Deaths'], 
                name='Deaths',
                line=dict(color='red')
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=country_data['ObservationDate'], 
                y=country_data['Recovered'], 
                name='Recovered',
                line=dict(color='green')
            )
        )
        
        fig.update_layout(
            title=f'COVID-19 Trends in {selected_country}',
            xaxis_title='Date',
            yaxis_title='Count',
            legend_title='Metric',
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Top countries comparison
        st.subheader("Top Countries by Confirmed Cases")
        
        top_countries = latest_data.sort_values('Confirmed', ascending=False).head(10)
        
        fig = px.bar(
            top_countries,
            x='Country',
            y='Confirmed',
            color='Deaths',
            title='Top 10 Countries by Confirmed Cases',
            labels={'Confirmed': 'Confirmed Cases', 'Deaths': 'Deaths'},
            color_continuous_scale=px.colors.sequential.Reds
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # World map
        st.subheader("Global Case Distribution")
        
        fig = px.choropleth(
            latest_data,
            locations="Country",
            locationmode='country names',
            color="Confirmed",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Plasma,
            title="Confirmed Cases by Country"
        )
        
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    # Continental Trends page
    elif page == "Continental Trends":
        st.header("COVID-19 Trends by Continent")
        
        # Continental comparison chart
        st.subheader("Case Progression by Continent")
        
        fig = px.line(
            continent_data,
            x='ObservationDate',
            y='Confirmed',
            color='Continent',
            title='Cases by Continent Over Time',
            line_group='Continent',
            hover_name='Continent'
        )
        
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Confirmed Cases',
            legend_title='Continent',
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Latest cases by continent
        st.subheader("Current Cases by Continent")
        
        latest_continent_data = continent_data[continent_data['ObservationDate'] == continent_data['ObservationDate'].max()]
        
        fig = px.pie(
            latest_continent_data,
            values='Confirmed',
            names='Continent',
            title='Distribution of Cases by Continent',
            hole=0.3
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Mortality by continent
        st.subheader("Mortality Rate by Continent")
        
        latest_continent_data['Mortality_Rate'] = (latest_continent_data['Deaths'] / latest_continent_data['Confirmed'] * 100).round(2)
        
        fig = px.bar(
            latest_continent_data,
            x='Continent',
            y='Mortality_Rate',
            color='Mortality_Rate',
            title='Mortality Rate by Continent',
            labels={'Mortality_Rate': 'Mortality Rate (%)'},
            color_continuous_scale=px.colors.sequential.Reds
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Mortality Analysis page
    elif page == "Mortality Analysis":
        st.header("COVID-19 Mortality Analysis")
        
        # High mortality countries
        st.subheader("Countries with Highest Mortality Rates")
        
        # Filter countries with at least 1000 cases
        high_mortality = latest_data[latest_data['Confirmed'] > 1000].sort_values('Mortality_Rate', ascending=False).head(10)
        
        fig = px.bar(
            high_mortality,
            x='Country',
            y='Mortality_Rate',
            title='Top 10 Countries by Mortality Rate (1000+ cases)',
            color='Mortality_Rate',
            labels={'Mortality_Rate': 'Mortality Rate (%)'},
            color_continuous_scale=px.colors.sequential.Reds
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Global mortality trend
        st.subheader("Global Mortality Rate Over Time")
        
        global_data['Mortality_Rate'] = (global_data['Deaths'] / global_data['Confirmed'] * 100).round(2)
        
        fig = px.line(
            global_data,
            x='ObservationDate',
            y='Mortality_Rate',
            title='Global Mortality Rate Trend',
            labels={'Mortality_Rate': 'Mortality Rate (%)'}
        )
        
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Mortality Rate (%)',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Scatter plot of cases vs deaths
        st.subheader("Relationship Between Cases and Deaths")
        
        fig = px.scatter(
            latest_data[latest_data['Confirmed'] > 1000],
            x='Confirmed',
            y='Deaths',
            color='Continent',
            hover_name='Country',
            size='Confirmed',
            log_x=True,
            log_y=True,
            title='Cases vs Deaths by Country (log scale)',
            trendline='ols',
            labels={'Confirmed': 'Confirmed Cases (log)', 'Deaths': 'Deaths (log)'}
        )
        
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.error("Please make sure the 'covid_19_data.csv' file is in the same directory as this app.")
    st.info("You can download the dataset from: https://www.kaggle.com/datasets/sheshngupta/covid19-global-dashboard")