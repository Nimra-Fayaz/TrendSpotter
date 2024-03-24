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
        response = model.generate_content(prompt)
        top_trends = [trend.content.parts[0].text for trend in response.candidates]
        return top_trends
    except Exception as e:
        st.error(f"Error fetching trends: {e}")
        return []

# Function to generate social media post using Gemini
def generate_social_media_post(trends, platform):
    try:
        posts = []
        for trend in trends:
            prompt = f"Write an educational and attractive social media post about '{trend}' individually for each trend for {platform} using proper hashtags."
            response = model(prompt)
            post = response.candidates[0].content.parts[0].text
            posts.append(post)
        return posts
    except Exception as e:
        st.error(f"Error generating social media posts: {e}")
        return []

# Main content area
st.title("Social Media Trends Dashboard")

# Assuming the UI has a sidebar for filters
with st.sidebar:
    st.title("Filters")
    region = st.selectbox("Select Region", ["Worldwide", "United States", "United Kingdom", "India", "Pakistan", "Canada", "Australia", "France", "Germany", "Russia"])
    show_trends_button = st.button("Show Trends")

    # Dropdown for selecting social media platform
    platform = st.selectbox("Select Social Media Platform", ["X", "Instagram", "Facebook", "LinkedIn"])
    generate_post_button = st.button("Generate Post")

# Fetch and display top 3 trends for the selected region
if show_trends_button:
    top_trends = get_top_trends(region)
    if top_trends:
        st.write("Top 3 Trends:")
        for trend in top_trends:
            st.write(f"- {trend}")

# Generate social media posts for the selected platform
if generate_post_button:
    if "top_trends" in locals():
        if top_trends:
            posts = generate_social_media_post(top_trends, platform)
            if posts:
                st.write("Generated Posts:")
                for index, post in enumerate(posts, start=1):
                    st.write(f"Post {index}:")
                    st.write(post)
    else:
        st.warning("Please show trends first before generating posts.")
