import streamlit as st
import google.generativeai as genai

# Set page layout configuration
st.set_page_config(layout="wide")

# Set up Google Generative AI client
genai.configure(api_key="AIzaSyBCL92zWhFPocMHLd2Df2KSPbKWCRCYTSQ") 
model = genai.GenerativeModel('gemini-1.0-pro')

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


       
