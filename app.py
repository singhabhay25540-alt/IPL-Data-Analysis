import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 

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

st.sidebar.markdown("---")

st.sidebar.write("Select an IPL Team")

st.sidebar.markdown("---")

teams = sorted(df["winner"].dropna().unique())

selected_team = st.sidebar.selectbox(
    "Select a Team",
    ["All Teams"] + teams
)

# ---------------- COLOR CHANGE ---------------- #
bg = "#1f77b4"

if selected_team != "All Teams":
    bg = team_colors.get(selected_team, "#1f77b4")

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
    filtered_df = df[
        (df["team1"] == selected_team) |
        (df["team2"] == selected_team)
    ]

# ---------------- KPI CARDS ---------------- #

col1, col2, col3 = st.columns(3)

if selected_team == "All Teams":

    matches = len(df)
    wins = df["winner"].count()
    win_percent = "-"

else:

    matches = len(filtered_df)

    wins = len(df[df["winner"] == selected_team])

    losses = matches - wins

    if matches > 0:
        win_percent = round((wins / matches) * 100, 2)
    else:
        win_percent = 0
        win_percent = 0

col1.metric("Matches Played", matches)
col2.metric("Matches Won", wins)
col3.metric("Win %", f"{win_percent}%")

st.divider()

# ---------------- DATASET ---------------- #
st.info("Use the sidebar to explore IPL team statistics.")

# ---------------- TEAM WINS GRAPH ---------------- #
if selected_team == "All Teams":
    st.subheader("🏆 Overall IPL Team Wins")
else:
    st.subheader(f"🏆 {selected_team} Match Wins")

if selected_team == "All Teams":
    team_wins = df["winner"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10,5))
    team_wins.plot(kind="bar", color="royalblue", ax=ax)

    plt.xticks(rotation=45)
    plt.xlabel("Teams")
    plt.ylabel("Wins")
    plt.grid(axis="y", alpha=0.3)

    st.pyplot(fig)

else:
    season_wins = (
        filtered_df.groupby("season")
        .size()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(10,5))
    season_wins.plot(
        kind="bar",
        color=bg,
        ax=ax
    )

    plt.xticks(rotation=45)
    plt.xlabel("Season")
    plt.ylabel("Matches Won")
    plt.grid(axis="y", alpha=0.3)

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

st.markdown("---")
st.subheader("🥇 Top 10 Player of the Match Winners")

pom = df['player_of_match'].value_counts().head(10)

fig3, ax3 = plt.subplots(figsize=(10,5))
pom.plot(kind='bar', ax=ax3)

plt.xticks(rotation=45)
plt.xlabel("Players")
plt.ylabel("Awards")
plt.title("Top 10 Player of the Match Winners")

st.pyplot(fig3)

st.markdown("---")
st.subheader("🏟️ Top 10 IPL Venues")

venue = df["venue"].value_counts().head(10).reset_index()
venue.columns = ["Venue", "Matches"]

fig4 = px.bar(
    venue,
    x="Venue",
    y="Matches",
    text="Matches",
    title="Top 10 IPL Venues"
)

fig4.update_traces(
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>Matches: %{y}<extra></extra>"
)

fig4.update_layout(
    xaxis=dict(tickangle=-30),
    yaxis_title="Matches",
    xaxis_title="Venue",
    height=600
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("🌍 Top Cities Hosting IPL Matches")

city = df["city"].value_counts().head(10).reset_index()
city.columns = ["City", "Matches"]

fig5 = px.bar(
    city,
    x="City",
    y="Matches",
    text="Matches",
    title="Top Cities Hosting IPL Matches"
)

fig5.update_traces(
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>Matches: %{y}<extra></extra>"
)

fig5.update_layout(
    xaxis_title="City",
    yaxis_title="Matches",
    xaxis=dict(tickangle=-20),
    height=550
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.subheader("🪙 Toss Decision Analysis")

toss = df['toss_decision'].value_counts()

fig6, ax6 = plt.subplots(figsize=(6,6))
ax6.pie(toss, labels=toss.index, autopct="%1.1f%%", startangle=90)
ax6.set_title("Bat First vs Field First")

st.pyplot(fig6)

st.markdown("---")

st.markdown(
"""
<center>

Made with ❤️ by <b>Abhay Singh</b>

BS in Data Science | IIT Madras

</center>
""",
unsafe_allow_html=True
)
