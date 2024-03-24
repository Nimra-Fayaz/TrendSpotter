import streamlit as st
import google.generativeai as genai

# Set page layout configuration
st.set_page_config(layout="wide")

# Set up Google Generative AI client
genai.configure(api_key="AIzaSyBZo_OCHYHslSXuwtaPNjLavGnfQaZ4kd0")  # Replace YOUR_API_KEY with your actual API key
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# Function to fetch top 3 trends for the selected region using Gemini
def get_top_trends(region):
    try:
        # Construct a prompt to fetch top trends for the selected region
        prompt = f"Show top 3 trends in {region}"
        
        # Generate text using Gemini
        top_trends = model.query(prompt, max_tokens=50, temperature=0.7)
        
        # Extract top trends from the response
        trends_list = top_trends['output'][0]['tokens']
        
        # Convert the tokens to a list of trends
        trends = [' '.join(token['value'] for token in trend) for trend in trends_list]
        
        return trends
    except Exception as e:
        st.error(f"Error fetching trends: {e}")
        return []

# Main content area
st.title("Social Media Trends Dashboard")

# Assuming the UI has a sidebar for filters
with st.sidebar:
    st.title("Filters")
    region = st.selectbox("Select Region", ["Worldwide", "United States", "United Kingdom", "India"])
    show_trends_button = st.button("Show Trends")

# Fetch and display top 3 trends for the selected region when the button is clicked
if show_trends_button:
    top_trends = get_top_trends(region)
    if top_trends:
        st.write(f"Top 3 Trending Topics in {region}:")
        for trend in top_trends:
            st.write(f"- {trend}")

# Right column for content of posts
st.header("Generate Post")
if top_trends:
    selected_trend = st.selectbox("Select Trend", top_trends)
    selected_platform = st.selectbox("Select Platform", ["Twitter", "Facebook", "Instagram", "LinkedIn"])
    button = st.button("Generate Post")
    if button:
        try:
            # Generate a post based on the selected trend and platform using Gemini
            post_prompt = f"Write a social media post with relevant hashtags about the trending topic '{selected_trend}' for {selected_platform}"
            post_text = model.query(post_prompt, max_tokens=100, temperature=0.7)
            st.markdown(f"**{selected_platform}**")
            st.markdown(post_text['output'][0]['text'])
        except Exception as e:
            st.error(f"Error generating post: {e}")
