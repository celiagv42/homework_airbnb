import streamlit as st
import pandas as pd
import plotly.express as px

# I configure the page 
st.set_page_config(layout="wide", page_title="Airbnb Dashboard")

# Loading my data
df = pd.read_csv("airbnb.csv")

# Removing NaN values 
df = df.dropna(subset=["price", "reviews_per_month", "latitude", "longitude"])

# Sidebar for filters
st.sidebar.header("Data Filters")
neighbourhood_group = st.sidebar.multiselect("Select a zone:", df["neighbourhood_group"].unique())
type_listings = st.sidebar.multiselect("Select listing type:", df["room_type"].unique())

# Applying filters
if neighbourhood_group:
    df = df[df["neighbourhood_group"].isin(neighbourhood_group)]
if type_listings:
    df = df[df["room_type"].isin(type_listings)]

# I Create 2 tabs
tab1, tab2 = st.tabs(["Data Analysis", "Advanced Visualization"])

with tab1:
    st.header("Data Exploration")
    st.dataframe(df.head())
    
    # Chart 1: Relationship between listing type and price
    st.subheader("Relationship between Listing Type and Price")
    fig1 = px.bar(df.groupby("room_type")["price"].mean().reset_index(), x="room_type", y="price", title="Average Price per Listing Type")
    st.plotly_chart(fig1)
    
    # Chart 2: Price distribution by listing type
    st.subheader("Price Distribution by Listing Type")
    fig2 = px.box(df, x="room_type", y="price", title="Price Distribution by Listing Type")
    st.plotly_chart(fig2)

with tab2:
    st.header("Advanced Visualization")
    
    # Chart 3: Relationship between number of reviews and price (Handle NaN values)
    st.subheader("Relationship between Number of Reviews and Price")
    df_filtered_reviews = df.dropna(subset=["reviews_per_month", "price"]) 
    fig3 = px.scatter(df_filtered_reviews, x="reviews_per_month", y="price", size="price", color="neighbourhood_group", title="Number of Reviews vs Price")
    st.plotly_chart(fig3)
    
    # Map of listings
    st.subheader("Map of Airbnb Listings")
    st.map(df.dropna(subset=["latitude", "longitude"]))

# Optional Price Simulator 
st.sidebar.subheader("Price Simulator")
neigh_sim = st.sidebar.selectbox("Select a neighborhood:", df["neighbourhood"].unique())
type_sim = st.sidebar.selectbox("Select listing type:", df["room_type"].unique())
people_sim = st.sidebar.slider("Number of guests:", min_value=1, max_value=10, value=2)

# Filtering relevant data
df_filtered = df[(df["neighbourhood"] == neigh_sim) & (df["room_type"] == type_sim)]
price_range = df_filtered["price"].mean()

if not df_filtered.empty:
    st.sidebar.write(f"Recommended Price: **€{price_range:.2f}**")
else:
    st.sidebar.write("Not enough data to recommend a price.")
