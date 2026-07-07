import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE SETTINGS ---------------- #
st.set_page_config(page_title="IPL Data Analysis Dashboard",
                   page_icon="🏏",
                   layout="wide")

# ---------------- LOAD DATA ---------------- #
df = pd.read_csv("ipl_comprehensive_dataset.csv")

# ---------------- TEAM COLORS ---------------- #
team_colors = {
    "Mumbai Indians":"#004BA0",
    "Chennai Super Kings":"#E6B800",
    "Royal Challengers Bengaluru":"#8B0000",
    "Royal Challengers Bangalore":"#8B0000",
    "Kolkata Knight Riders":"#3B0A57",
    "Delhi Capitals":"#003F87",
    "Punjab Kings":"#B71C1C",
    "Kings XI Punjab":"#B71C1C",
    "Rajasthan Royals":"#7D3C98",
    "Sunrisers Hyderabad":"#D35400",
    "Lucknow Super Giants":"#0B5394",
    "Gujarat Titans":"#0F4C81"
}

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🏏 IPL Dashboard")

teams = sorted(df["winner"].dropna().unique())

selected_team = st.sidebar.selectbox(
    "Select a Team",
    ["All Teams"] + teams
)

# ---------------- COLOR CHANGE ---------------- #
bg = "#ffffff"

if selected_team != "All Teams":
    bg = team_colors.get(selected_team, "#ffffff")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color:{bg}15;
    }}
    h1,h2,h3 {{
        color:{bg};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TITLE ---------------- #
st.title("🏏 IPL Data Analysis Dashboard")
st.write("Interactive Analysis of IPL Matches")

# ---------------- DATA FILTER ---------------- #
if selected_team == "All Teams":
    filtered_df = df
else:
    filtered_df = df[df["winner"] == selected_team]

# ---------------- KPI CARDS ---------------- #
col1, col2, col3 = st.columns(3)

matches = len(filtered_df)
wins = filtered_df["winner"].count()

if selected_team == "All Teams":
    win_percent = "-"
else:
    total_matches = len(df[(df["team1"] == selected_team) | (df["team2"] == selected_team)])
    win_percent = round((wins/total_matches)*100,2) if total_matches else 0

col1.metric("Matches", matches)
col2.metric("Wins", wins)
col3.metric("Win %", win_percent)

st.divider()

# ---------------- DATASET ---------------- #
st.subheader("Dataset Preview")
st.dataframe(filtered_df, use_container_width=True)

# ---------------- TEAM WINS GRAPH ---------------- #
st.subheader(f"{selected_team} Performance Overview")

team_wins = filtered_df["winner"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10,5))

team_wins.plot(
    kind="bar",
    color=bg,
    ax=ax
)

plt.xticks(rotation=45)
plt.xlabel("Teams")
plt.ylabel("Wins")

st.pyplot(fig)

# ---------------- MATCHES PER SEASON ---------------- #

st.subheader("Matches Played Per Season")

season = filtered_df["season"].value_counts().sort_index()

fig2, ax2 = plt.subplots(figsize=(10,5))

season.plot(
    kind="line",
    marker="o",
    linewidth=3,
    color=bg,
    ax=ax2
)
ax2.set_xticks(range(len(season.index)))
ax2.set_xticklabels(season.index, rotation=45)

plt.grid(True)

plt.xlabel("Season")
plt.ylabel("Matches")

st.pyplot(fig2)

st.success("Created by Abhay Singh ❤️")
