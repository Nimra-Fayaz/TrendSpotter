import streamlit as st
from bs4 import BeautifulSoup
import requests
import google.generativeai as genai

#AI Model
genai.configure(api_key="AIzaSyBZo_OCHYHslSXuwtaPNjLavGnfQaZ4kd0")
model = genai.GenerativeModel('gemini-1.0-pro-latest')

#Scraping function
def scrape_trends(region):
  url = f"https://trends.google.com/trends/explore?geo={region}"
  response = requests.get(url)
  soup = BeautifulSoup(response.text,'html.parser')  
  trends_div = soup.find("div", class_="...")

  trends = []
  for a in trends_div.find_all("a"):
    trends.append(a.text)

  return trends[:3]

#UI
st.title("Trends Dashboard")

region = st.selectbox("Select Region") 

if st.button("Get Trends"):
  trends = scrape_trends(region)
  for trend in trends:
    st.write(trend)

platforms = st.multiselect("Platforms")
selected_trend = st.selectbox("Trend", trends) 

if st.button("Generate Posts"):
  for platform in platforms:
    prompt = f"Write an educational social media post about trend '{selected_trend}' for {platform}"
    post = model.generate_text(prompt)
    st.write(post)
