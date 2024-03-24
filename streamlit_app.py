import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import subprocess
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError

# Set page layout configuration
st.set_page_config(layout="wide")

# Variables for trends and platforms
Trends = ['Trend 1', 'Trend 2', 'Trend 3']
Trend_values = [0, 0, 0]
platforms_list = ["Twitter", "Facebook", "Instagram", "LinkedIn"]

# Set up Google Generative AI client
genai.configure(api_key="AIzaSyBZo_OCHYHslSXuwtaPNjLavGnfQaZ4kd0")  # Replace with your actual API key
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# Set up Google Trends
pytrend = TrendReq()

# Get the available regions from Google Trends
try:
    regions = pytrend.build_payload(kw_list=[], geo='').geo.tolist()
except ResponseError as e:
    st.error(f"Error fetching regions: {e}")
    regions = []

# Function to generate posts with hashtags
def generate_posts(selected_trends, region, selected_platforms):
    for trend in selected_trends:
        try:
            # Fetch the latest trend for the specified region
            trend_payload = pytrend.trending_searches(pn=region.lower())
            latest_trend = trend_payload.values[0][0]

            for platform in selected_platforms:
                # Generate a post based on the latest trend and platform
                post_prompt = f"Write a social media post with relevant hashtags about the trending topic '{latest_trend}' for {platform}"
                post_text = model.generate_text(post_prompt)
                st.markdown(f"**{platform}**")
                st.markdown(post_text)
                st.markdown("---")
        except ResponseError as e:
            st.error(f"Error generating posts: {e}")

def for_each_platform(platforms_number):
    for idx, platform in enumerate(platforms_number):
        st.header(platform)
        navigate_to_posts(selected_trends)

def navigate_to_posts(selected_trends):
    cols = st.columns(len(selected_trends))
    i = 0

    for trend, col in zip(selected_trends, cols):
        with col:
            st.header(trend)

# Function to fetch and display trends
def show_trends(region):
    try:
        trend_payload = pytrend.trending_searches(pn=region.lower())
        trends = trend_payload.values[0]
        st.write(f"Top Trending Topics in {region}:")
        for trend in trends:
            st.write(f"- {trend}")
    except ResponseError as e:
        st.error(f"Error fetching trends: {e}")

# Assuming the UI has a sidebar for filters
with st.sidebar:
    st.title("Filters")
    region = st.selectbox("Select Region", regions)
    platforms = st.multiselect("Select Platforms", platforms_list)
    show_trends_button = st.button("Show Trends")
    if show_trends_button:
        show_trends(region)

# Main content area
st.title("Social Media Trends Dashboard")

# Split main content area into two sections
left_column, right_column = st.columns(2)

# Left column for round graphs
with left_column:
    st.header("Trend Visuals")
    chart_data = {Trends[0]: Trend_values[0], Trends[1]: Trend_values[1], Trends[2]: Trend_values[2]}
    st.write("Analytics")
    st.bar_chart(chart_data)

# Right column for content of posts
with right_column:
    st.header("Trend Posts")
    selected_trends = st.multiselect("Select Trends", Trends)
    button = st.button("Generate Posts")
    if button:
        generate_posts(selected_trends, region, platforms)
        for_each_platform(platforms)
