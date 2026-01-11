import streamlit as st
import json
import requests
import pandas as pd

st.set_page_config(
    page_title="NPTEL Course Stats Explorer",
    layout="wide",
)

# ---- minimal CSS ----
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
    }
    .card {
        background-color: #111827;
        padding: 1.25rem;
        border-radius: 10px;
        border: 1px solid #1f2937;
        margin-bottom: 1.5rem;
    }
    .metric {
        font-size: 1.6rem;
        font-weight: 600;
    }
    .metric-label {
        color: #9ca3af;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- load data ----
with open("filtered_courses.json", "r", encoding="utf-8") as f:
    data = json.load(f)

courses = data["courses"]
for c in courses:
    c["title_lower"] = c["title"].lower()

st.title("NPTEL Course Stats Explorer")

# ---- search ----
st.markdown('<div class="card">', unsafe_allow_html=True)
query = st.text_input("Course name", placeholder="Type part of the course title")
st.markdown("</div>", unsafe_allow_html=True)

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
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


if selected_course:
    course_id = selected_course["id"]

    if "last_course_id" not in st.session_state:
        st.session_state.last_course_id = None

    if st.session_state.last_course_id != course_id:
        st.session_state.last_course_id = course_id

        with st.spinner("Fetching stats..."):
            stats = fetch_course_stats(course_id)

        rows = []

        for course in stats.get("data", []):
            for r in course.get("run_wise_stats", []):
                rows.append(
                    {
                        "Timeline": r.get("Timeline", ""),
                        "Max Mark": float(r.get("max_mark", 0)),
                        "Min Mark": float(r.get("min_mark", 0)),
                        "Average": float(r.get("average", 0)),
                        "Std Deviation": float(r.get("standard_deviation", 0)),
                    }
                )

        if rows:
            df = pd.DataFrame(rows)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Summary")

            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(
                f"<div class='metric'>{df['Max Mark'].max()}</div><div class='metric-label'>Max Mark</div>",
                unsafe_allow_html=True,
            )
            c2.markdown(
                f"<div class='metric'>{df['Min Mark'].min()}</div><div class='metric-label'>Min Mark</div>",
                unsafe_allow_html=True,
            )
            c3.markdown(
                f"<div class='metric'>{df['Average'].mean():.2f}</div><div class='metric-label'>Mean Average</div>",
                unsafe_allow_html=True,
            )
            c4.markdown(
                f"<div class='metric'>{df['Std Deviation'].mean():.2f}</div><div class='metric-label'>Mean Std Dev</div>",
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Run-wise Statistics")
            st.dataframe(df, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No run-wise statistics available")
