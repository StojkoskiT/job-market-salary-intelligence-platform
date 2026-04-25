import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Job Market Salary Intelligence", layout="wide")

df = pd.read_csv(r"C:\Users\T\Documents\job-market-salary-intelligence-platform\data\raw\ds_salaries.csv")

st.title("Job Market & Salary Intelligence Platform")
st.write("Analyze salary trends, remote work patterns, experience levels, and salary insights for data roles.")

st.sidebar.header("Filters")

experience_options = sorted(df["experience_level"].unique())

selected_experience = st.sidebar.multiselect(
    "Experience Level",
    experience_options,
    default=experience_options
)

filtered_df = df[df["experience_level"].isin(selected_experience)]

col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(filtered_df))
col2.metric("Average Salary", f"${filtered_df['salary_in_usd'].mean():,.0f}")
col3.metric("Remote Jobs", len(filtered_df[filtered_df["remote_ratio"] == 100]))

st.subheader("Top Paying Job Titles")

top_jobs = (
    filtered_df.groupby("job_title")["salary_in_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10, 6))
top_jobs.sort_values().plot(kind="barh", ax=ax)
ax.set_xlabel("Average Salary (USD)")
ax.set_ylabel("Job Title")
st.pyplot(fig)

st.subheader("Salary by Experience Level")

salary_exp = filtered_df.groupby("experience_level")["salary_in_usd"].mean()

fig2, ax2 = plt.subplots(figsize=(8, 5))
salary_exp.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Average Salary (USD)")
st.pyplot(fig2)

st.subheader("Remote Work Distribution")

remote_counts = filtered_df["remote_ratio"].value_counts().sort_index()

fig3, ax3 = plt.subplots(figsize=(8, 5))
remote_counts.plot(kind="bar", ax=ax3)
ax3.set_xlabel("Remote Ratio")
ax3.set_ylabel("Number of Jobs")
st.pyplot(fig3)

st.subheader("Raw Data")
st.dataframe(filtered_df)