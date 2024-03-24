import streamlit as st
import google.generativeai as genai

# Set page layout configuration
st.set_page_config(layout="wide")

# Set up Google Generative AI client
genai.configure(api_key="AIzaSyBCL92zWhFPocMHLd2Df2KSPbKWCRCYTSQ") 
model = genai.GenerativeModel('gemini-1.0-pro')

# Function to fetch top 3 trends for the selected region using Gemini
def get_top_trends(region):
    try:
        prompt = f"Show top 3 trends in {region} which people are searching for, get data from the google trends"
        trends = model.generate_content(prompt)
        return trends
    except Exception as e:
        st.error(f"Error fetching trends: {e}")
        return []

# Function to generate social media post using Gemini
def generate_social_media_post(trends, platform):
    try:
        prompt = f"Write an educational and attractive social media post about '{trends}' individually for each trend for {platform} using proper hashtags."
        post = model.generate_content(prompt)
        return post
    except Exception as e:
        st.error(f"Error generating social media post: {e}")
        return ""

# Main content area
st.title("Social Media Trends Dashboard")

# Assuming the UI has a sidebar for filters
with st.sidebar:
    st.title("Filters")
    region = st.selectbox("Select Region", ["Worldwide", "United States", "United Kingdom", "India", "Pakistan", "Canada", "Australia", "France", "Germany", "Russia"])
    show_trends_button = st.button("Show Trends")

# Fetch and display top 3 trends for the selected region
if show_trends_button:
    top_trends = get_top_trends(region)
    if top_trends:
        st.write("Top 3 Trends:")
        st.write(top_trends)
        selected_platform = st.selectbox("Select Platform", ["Twitter", "Facebook", "Instagram", "LinkedIn"])
        generate_post_button = st.button("Generate Post")
        if generate_post_button:
            social_media_post = generate_social_media_post(top_trends, selected_platform)
            if social_media_post:
                st.write("Generated Social Media Post:")
                st.write(social_media_post)
            else:
                st.warning("Failed to generate social media post.")
        else:
            st.info("Please press the 'Generate Post' button to generate social media post.")
    else:
        st.warning("No trends found for the selected region.")
else:
    st.info("Press the 'Show Trends' button to fetch top trends for the selected region.")

