import numpy as np
import pandas as pd
import streamlit as st
import geopandas as gpd
from overturemaps import core
from io import StringIO

# Set page title
st.title("Business Phone Number Scraper")

# Input for bounding box coordinates
st.subheader("Feeling short on leads? This tool allows the user to designate a boundary box, select business categories, and find the phone numbers of businesses in said categories with no listed website. Powered by Overture Maps, an open source geospatial comapny. Quick, easy, free to use!")
st.write("---")
st.write("Default boundary box set to SF, map visualization coming soon!\nFor a quick demo, simply press the \"Scrape Business Phone Numbers\" Button at the bottom of this page.")
st.header("Bounding Box Coordinates")
col1, col2 = st.columns(2)
with col1:
  min_lon = st.number_input("Min Longitude", value=-122.66)
  min_lat = st.number_input("Min Latitude", value=37.0)
with col2:
  max_lon = st.number_input("Max Longitude", value=-121.6)
  max_lat = st.number_input("Max Latitude", value=38.0)

# Default bounding box
default_bbox = (-122.66, 37.0, -121.6, 38.0)
bbox = (min_lon, min_lat, max_lon, max_lat)

# Input for categories
st.header("Business Categories")
default_categories = ["cafe", "restaurant", "car_dealer", "florist"]
categories_input = st.text_area("Enter categories (one per line)", "\n".join(default_categories))
categories = [cat.strip() for cat in categories_input.split("\n") if cat.strip()]

if st.button("High Confidence Search"):
  with st.spinner("Fetching data from Overture Maps..."):
    try:
      gdf = core.geodataframe("place", bbox=bbox)
      gdf_high_conf = gdf[gdf['confidence'] >= 0.9]
      
      biz_high_conf = gdf_high_conf[gdf_high_conf.columns[7]]
      biz_primary_hc = biz_high_conf.apply(lambda x: x.get('primary', 'N/A'))
      biz_phones_hc = gdf_high_conf[gdf_high_conf.columns[12]]

      phones = []
      results = {}

      for category in categories:
        phone = []
        for i in range(len(biz_high_conf)):
          if biz_primary_hc[i] == category and gdf_high_conf[gdf_high_conf.columns[9]][i] is None:
            if biz_phones_hc[i] is not None:
              phone.append(biz_phones_hc[i])
        
        phones.append(phone)
        results[category] = phone
        st.write(f"Number of phone numbers found for {category} businesses without websites: {len(phone)}")
      
      # Display phone numbers
      st.header("Results")
      
      for idx, category in enumerate(categories):
        if phones[idx]:
          st.subheader(f"{category.capitalize()} Phone Numbers")
          phone_df = pd.DataFrame({"Phone": [p[0] for p in phones[idx] if p and len(p) > 0]})
          st.dataframe(phone_df)
          
          # Download button for each category
          csv = phone_df.to_csv(index=False)
          st.download_button(
            label=f"Download {category} phone numbers",
            data=csv,
            file_name=f"{category}_phones.csv",
            mime="text/csv"
          )
      
      # Download all data as one file
      all_phones = {}
      for idx, category in enumerate(categories):
        if phones[idx]:
          all_phones[category] = [p[0] for p in phones[idx] if p and len(p) > 0]
      
      all_df = pd.DataFrame({cat: pd.Series(all_phones.get(cat, [])) for cat in categories})
      csv = all_df.to_csv(index=False)
      st.download_button(
        label="Download all phone numbers",
        data=csv,
        file_name="all_business_phones.csv",
        mime="text/csv"
      )
        
    except Exception as e:
      st.error(f"An error occurred: {str(e)}")


# Process button
st.write("Click me!")
if st.button("Scrape Business Phone Numbers"):
  with st.spinner("Fetching data from Overture Maps..."):
    try:
      # Get geodataframe
      gdf = core.geodataframe("place", bbox=bbox)
      # Extract business data
      biz = gdf[gdf.columns[7]]
      biz_primary = biz.apply(lambda x: x.get('primary', 'N/A'))
      biz_phones = gdf[gdf.columns[12]]

      # Process phone numbers by category
      phones = []
      results = {}
      
      for category in categories:
        phone = []
        for i in range(len(biz)):
          if biz_primary[i] == category and gdf[gdf.columns[9]][i] is None:
            if biz_phones[i] is not None:
              phone.append(biz_phones[i])
        
        phones.append(phone)
        results[category] = phone
        st.write(f"Number of phone numbers found for {category} businesses without websites: {len(phone)}")
      
      # Display phone numbers
      st.header("Results")
      
      for idx, category in enumerate(categories):
        if phones[idx]:
          st.subheader(f"{category.capitalize()} Phone Numbers")
          phone_df = pd.DataFrame({"Phone": [p[0] for p in phones[idx] if p and len(p) > 0]})
          st.dataframe(phone_df)
          
          # Download button for each category
          csv = phone_df.to_csv(index=False)
          st.download_button(
            label=f"Download {category} phone numbers",
            data=csv,
            file_name=f"{category}_phones.csv",
            mime="text/csv"
          )
      
      # Download all data as one file
      all_phones = {}
      for idx, category in enumerate(categories):
        if phones[idx]:
          all_phones[category] = [p[0] for p in phones[idx] if p and len(p) > 0]
      
      all_df = pd.DataFrame({cat: pd.Series(all_phones.get(cat, [])) for cat in categories})
      csv = all_df.to_csv(index=False)
      st.download_button(
        label="Download all phone numbers",
        data=csv,
        file_name="all_business_phones.csv",
        mime="text/csv"
      )
        
    except Exception as e:
      st.error(f"An error occurred: {str(e)}")
st.write("Made with love by Cyrus Correll")
# Add some instructions
st.sidebar.header("Instructions")
st.sidebar.write("""
1. Set the bounding box coordinates
2. Enter the business categories you want to scrape
3. Click "Scrape Business Phone Numbers" 
4. Download the results as CSV files
""")
