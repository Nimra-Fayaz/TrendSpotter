import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import streamlit as st
import subprocess
from pytrends.request import TrendReq

# Variables for trends, countries, and platforms
Trends = ['Trend 1', 'Trend 2', 'Trend 3']
Trend_values = [0, 0, 0]
countries = ["Global", "USA", "India", "Others"]
platforms_list = ["Twitter", "Facebook", "Instagram", "LinkedIn"]

# Set up Google Generative AI client
genai.configure(api_key="your_genai_api_key")
model = genai.GenerativeModel('gemini-1.0-pro-vision-latest')

# Set up Google Trends
pytrend = TrendReq()

# Helper function to display text in Markdown format
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Function to generate posts with hashtags
def generate_posts(selected_trends, country, selected_platforms):
    for trend in selected_trends:
        # Fetch the latest trend for the specified country
        trend_payload = pytrend.trending_searches(pn=country.lower())
        latest_trend = trend_payload.values[0][0]

        for platform in selected_platforms:
            # Generate a post based on the latest trend and platform
            post_prompt = f"Write a social media post with relevant hashtags about the trending topic '{latest_trend}' for {platform}"
            post_text = model.generate_text(post_prompt)
            st.markdown(f"**{platform}**")
            st.markdown(post_text)
            st.markdown("---")

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

st.set_page_config(layout="wide")

# Assuming the UI has a sidebar for filters
with st.sidebar:
    st.title("Filters")
    country = st.selectbox("Select Country/Region", countries)
    platforms = st.multiselect("Select Platforms", platforms_list)
    b = st.button("Show trends")

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
        generate_posts(selected_trends, country, platforms)
        for_each_platform(platforms)
