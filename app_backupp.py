import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="IPL Data Analysis", layout="wide")

st.title("🏏 IPL Data Analysis Dashboard")
st.write("Analysis of IPL matches (2008–2026)")

# Load data
df = pd.read_csv("ipl_comprehensive_dataset.csv")

st.subheader("Dataset Preview")
st.dataframe(df, use_container_width=True)

st.subheader("Top 10 Teams by Wins")

wins = df['winner'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10,5))
wins.plot(kind='bar', ax=ax)
plt.xticks(rotation=45)
plt.xlabel("Teams")
plt.ylabel("Wins")
plt.title("Top 10 Teams by Wins")
st.pyplot(fig)

st.subheader("Matches Played Per Season")

season = df['season'].value_counts().sort_index()

fig2, ax2 = plt.subplots(figsize=(10,5))
season.plot(kind='line', marker='o', ax=ax2)
plt.xlabel("Season")
plt.ylabel("Matches")
plt.title("Matches Played Per Season")
st.pyplot(fig2)

st.success("Created by Abhay Singh")
