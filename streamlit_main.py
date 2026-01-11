import streamlit as st
import json
import requests

st.set_page_config(layout="wide")

with open("filtered_courses.json", "r", encoding="utf-8") as f:
    data = json.load(f)

courses = data["courses"]

for c in courses:
    c["title_lower"] = c["title"].lower()

st.title("NPTEL Course Stats Explorer")

query = st.text_input("Course")
results = []

if query:
    q = query.lower()
    results = [c for c in courses if q in c["title_lower"]]

selected_course = None

if results:
    options = {
        f"{c['title']} | {c['instituteName']} | {c['professor']}": c for c in results
    }
    selected_label = st.selectbox("Matching courses", options.keys())
    selected_course = options[selected_label]


@st.cache_data(show_spinner=False)
def fetch_course_stats(course_id):
    url = f"https://nptel.ac.in/api/stats/{course_id}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


if selected_course:
    if st.button("Fetch course stats"):
        with st.spinner("Fetching stats..."):
            stats = fetch_course_stats(selected_course["id"])

        runs = stats.get("data", [])
        if not runs:
            st.warning("No stats available")
        else:
            table_rows = []

            for run in runs:
                for r in run.get("run_wise_stats", []):
                    table_rows.append(
                        {
                            "Timeline": r.get("Timeline", ""),
                            "Max Mark": r.get("max_mark"),
                            "Min Mark": r.get("min_mark"),
                            "Average": r.get("average"),
                            "Standard Deviation": r.get("standard_deviation"),
                        }
                    )

            if table_rows:
                st.subheader("Run-wise Statistics")
                st.dataframe(table_rows, use_container_width=True)
            else:
                st.warning("No run-wise data found")
