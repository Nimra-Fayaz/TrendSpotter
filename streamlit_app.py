import requests
from bs4 import BeautifulSoup
import streamlit as st
import google.generativeai as genai
from pytrends.exceptions import ResponseError

# Set page layout configuration
st.set_page_config(layout="wide")

# Variables for trends and platforms
platforms_list = ["Twitter", "Facebook", "Instagram", "LinkedIn"]

# Set up Google Generative AI client
genai.configure(api_key="AIzaSyBZo_OCHYHslSXuwtaPNjLavGnfQaZ4kd0")  # Replace with your actual API key
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# Function to fetch top 3 trends for the selected region using web scraping
def get_top_trends(region):
    try:
        # Construct the URL for Google Trends based on the selected region
        url = f"https://trends.google.com/trends/trendingsearches/daily?geo={region}"
        
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the response
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the elements containing the trending topics
            trending_elements = soup.find_all('div', class_='details-text')
            
            # Extract the text of the trending topics
            trending_topics = [element.text.strip() for element in trending_elements][:3]  # Get top 3 trends
            
            return trending_topics
        else:
            # If the request failed, print an error message
            st.error(f"Failed to fetch trends. Status code: {response.status_code}")
            return None
    except Exception as e:
        # If an exception occurs, print the error message
        st.error(f"Error fetching trends: {e}")
        return None

# Main content area
st.title("Social Media Trends Dashboard")

# Assuming the UI has a sidebar for filters
with st.sidebar:
    st.title("Filters")
    region = st.selectbox("Select Region", ["Worldwide", "United States", "United Kingdom", "India"])
    show_trends_button = st.button("Show Trends")

# Fetch top 3 trends for the selected region
if show_trends_button:
    top_trends = get_top_trends(region.lower())
    if top_trends:
        st.write(f"Top 3 Trending Topics in {region}:")
        for trend in top_trends:
            st.write(f"- {trend}")

# Right column for content of posts
st.header("Generate Post")
selected_trend = st.selectbox("Select Trend", top_trends if top_trends else [])
selected_platform = st.selectbox("Select Platform", platforms_list)
button = st.button("Generate Post")
if button:
    if selected_trend and selected_platform:
        try:
            # Generate a post based on the selected trend and platform using Gemini
            post_prompt = f"Write a social media post with relevant hashtags about the trending topic '{selected_trend}' for {selected_platform}"
            post_text = model.generate_text(post_prompt)
            st.markdown(f"**{selected_platform}**")
            st.markdown(post_text)
        except Exception as e:
            st.error(f"Error generating post: {e}")
