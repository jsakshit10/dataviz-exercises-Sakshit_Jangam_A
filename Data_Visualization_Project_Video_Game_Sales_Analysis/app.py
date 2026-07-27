# Step 1

# 1 – Import Libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# 2 – Page Configuration
st.set_page_config(
    page_title="Video Game Sales Dashboard",
    page_icon="🎮",
    layout="wide"
)

# 3 – Dashboard Title
st.title("🎮 Video Game Sales Dashboard")

st.markdown("""
Interactive dashboard for analyzing global video game sales, genres,
platforms, publishers, and critic ratings.
""")

# 4 – Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Sakshit\Desktop\clg projects\SEM 2\Data Visualization\Project\Video_Games.csv")
    return df

games_df = load_data()
# Convert numeric columns
games_df["User_Score"] = pd.to_numeric(games_df["User_Score"], errors="coerce")
games_df["Critic_Score"] = pd.to_numeric(games_df["Critic_Score"], errors="coerce")
games_df["Global_Sales"] = pd.to_numeric(games_df["Global_Sales"], errors="coerce")

# 5 – Sidebar Filters
st.sidebar.header("Filters")

# Platform Filter
platform = st.sidebar.multiselect(
    "Select Platform",
    sorted(games_df["Platform"].dropna().unique()),
    default=sorted(games_df["Platform"].dropna().unique())
)

# Genre Filter
genre = st.sidebar.multiselect(
    "Select Genre",
    sorted(games_df["Genre"].dropna().unique()),
    default=sorted(games_df["Genre"].dropna().unique())
)

# Rating Filter
rating = st.sidebar.multiselect(
    "Select Rating",
    sorted(games_df["Rating"].dropna().unique()),
    default=sorted(games_df["Rating"].dropna().unique())
)

# 6 – Apply Filters
filtered_df = games_df[
    (games_df["Platform"].isin(platform)) &
    (games_df["Genre"].isin(genre)) &
    (games_df["Rating"].isin(rating))
]

# Step 2 – Add KPI Cards

filtered_df = games_df[
    (games_df["Platform"].isin(platform)) &
    (games_df["Genre"].isin(genre)) &
    (games_df["Rating"].isin(rating))
]

# KPI Calculations
# ============================
# KPI Calculations
# ============================

total_games = len(filtered_df)

total_sales = filtered_df["Global_Sales"].sum()

avg_critic = filtered_df["Critic_Score"].mean()

avg_user = filtered_df["User_Score"].mean()

# KPI Display
# ============================
# KPI Cards
# ============================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🎮 Total Games",
        value=f"{total_games:,}"
    )

with col2:
    st.metric(
        label="🌍 Global Sales",
        value=f"{total_sales:.2f} M"
    )

with col3:
    st.metric(
        label="⭐ Avg Critic Score",
        value=f"{avg_critic:.1f}"
    )

with col4:
    st.metric(
        label="👥 Avg User Score",
        value=f"{avg_user:.1f}"
    )

# Step 3 – Top 10 Platforms Chart
st.markdown("---")

st.subheader("🎮 Top 10 Platforms by Global Sales")

platform_sales = (
    filtered_df.groupby("Platform")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    platform_sales,
    x="Platform",
    y="Global_Sales",
    color="Global_Sales",
    text_auto=".1f",
    color_continuous_scale="Blues",
    title="Top 10 Platforms by Global Sales"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_title="Platform",
    yaxis_title="Global Sales (Millions)",
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)

# Step 4 – Top Genres Chart
st.markdown("---")

st.subheader("🎯 Top Genres by Global Sales")

genre_sales = (
    filtered_df.groupby("Genre")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    genre_sales,
    x="Genre",
    y="Global_Sales",
    color="Global_Sales",
    text_auto=".1f",
    color_continuous_scale="Greens",
    title="Global Sales by Genre"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_title="Genre",
    yaxis_title="Global Sales (Millions)",
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)

# Step 5 – Sales Trend Over Time
st.markdown("---")

st.subheader("📈 Global Sales Over Time")

sales_trend = (
    filtered_df.groupby("Year_of_Release")["Global_Sales"]
    .sum()
    .reset_index()
    .sort_values("Year_of_Release")
)

fig = px.line(
    sales_trend,
    x="Year_of_Release",
    y="Global_Sales",
    markers=True,
    title="Global Sales by Release Year"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_title="Release Year",
    yaxis_title="Global Sales (Millions)"
)

st.plotly_chart(fig, use_container_width=True)

# Step 6 – Scatter Plot (Critic Score vs Global Sales)
st.markdown("---")

st.subheader("⭐ Critic Score vs Global Sales")

scatter_df = filtered_df.dropna(
    subset=["Critic_Score", "Global_Sales"]
)

fig = px.scatter(
    scatter_df,
    x="Critic_Score",
    y="Global_Sales",
    color="Genre",
    hover_data=["Name"],
    opacity=0.7,
    title="Relationship Between Critic Score and Global Sales"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_title="Critic Score",
    yaxis_title="Global Sales (Millions)"
)

st.plotly_chart(fig, use_container_width=True)

# Step 7 – Platform × Genre Heatmap
st.markdown("---")

st.subheader("🔥 Platform vs Genre Heatmap")

heatmap_df = (
    filtered_df
    .groupby(["Platform", "Genre"])["Global_Sales"]
    .sum()
    .reset_index()
)

heatmap_data = heatmap_df.pivot(
    index="Platform",
    columns="Genre",
    values="Global_Sales"
).fillna(0)

fig = px.imshow(
    heatmap_data,
    color_continuous_scale="Blues",
    aspect="auto",
    title="Global Sales by Platform and Genre"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)

# Step 8 – Top 10 Publishers
st.markdown("---")

st.subheader("🏢 Top 10 Publishers")

publisher_sales = (
    filtered_df
    .groupby("Publisher")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    publisher_sales,
    x="Publisher",
    y="Global_Sales",
    color="Global_Sales",
    text_auto=".1f",
    color_continuous_scale="Purples",
    title="Top Publishers by Global Sales"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)

# Step 9 – Show the Filtered Data
st.markdown("---")

st.subheader("📄 Filtered Dataset")

st.dataframe(filtered_df)

# Step 10 – Download Filtered Data
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_video_games.csv",
    mime="text/csv"
)