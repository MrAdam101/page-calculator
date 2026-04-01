import streamlit as st
from datetime import date, timedelta
from utils.logic import get_teaching_dates, split_remaining_pages


st.set_page_config(
    page_title="Book Page Calculator",
    page_icon="📘",
    layout="wide"
)


def load_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("styles/main.css")


st.markdown('<div class="app-shell">', unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-icon">📘</div>
    <div>
        <h1>Book Page Calculator</h1>
        <p>
            Plan the remaining pages in seconds, based on your real teaching days.
            Built for busy teachers who need a clear catch-up plan that feels fast,
            reliable, and professional.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-card">
    <div class="section-title">Planning Inputs</div>
    <div class="section-subtitle">Enter your current progress and schedule to generate a polished catch-up plan.</div>
""", unsafe_allow_html=True)

book_name = st.text_input("Book Name", value="Start Right Reader 2")

col1, col2 = st.columns(2)
with col1:
    current_page = st.number_input("Current Page Completed", min_value=0, value=0, step=1)
with col2:
    last_page = st.number_input("Last Page in Book", min_value=1, value=60, step=1)

col3, col4 = st.columns(2)
with col3:
    start_date = st.date_input("Plan From Date", value=date.today())
with col4:
    end_date = st.date_input("Book End Date", value=date.today() + timedelta(days=30))

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
selected_days = st.multiselect(
    "Teaching Days Left",
    options=days_of_week,
    default=["Monday", "Wednesday", "Friday"],
)

calculate = st.button("Generate Catch-Up Plan")

st.markdown("</div>", unsafe_allow_html=True)

if calculate:
    if end_date < start_date:
        st.error("End date must be after the start date.")
    elif not selected_days:
        st.error("Please select at least one teaching day.")
    elif current_page > last_page:
        st.error("Current page cannot be greater than the last page.")
    elif current_page == last_page:
        st.success("You have already finished the book.")
    else:
        teaching_dates = get_teaching_dates(start_date, end_date, selected_days)
        lessons_left = len(teaching_dates)

        if lessons_left == 0:
            st.warning("There are no teaching days left in that date range.")
        else:
            page_plan, pages_left = split_remaining_pages(current_page, last_page, lessons_left)
            avg_pages = pages_left / lessons_left

            st.markdown("""
            <div class="section-card">
                <div class="section-title">Planning Dashboard</div>
                <div class="section-subtitle">Your key teaching targets at a glance.</div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-label">Pages Left</div>
                    <div class="kpi-value">{pages_left}</div>
                    <div class="kpi-note">Remaining from current progress</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Lessons Left</div>
                    <div class="kpi-value">{lessons_left}</div>
                    <div class="kpi-note">Based on selected teaching days</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Avg Pages / Lesson</div>
                    <div class="kpi-value">{avg_pages:.2f}</div>
                    <div class="kpi-note">Average needed to finish on time</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Next Page</div>
                    <div class="kpi-value">{current_page + 1}</div>
                    <div class="kpi-note">Where your next lesson begins</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="summary-wrap">
                <div class="summary-item">
                    <div class="summary-label">Book</div>
                    <div class="summary-value">{book_name}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Teaching Days</div>
                    <div class="summary-value">{", ".join(selected_days)}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Planning Window</div>
                    <div class="summary-value">{start_date} → {end_date}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Progress</div>
                    <div class="summary-value">Completed up to page {current_page}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div class="section-title">Lesson Plan</div>
                <div class="section-subtitle">A structured breakdown of what to cover each lesson.</div>
                <div class="plan-list">
            """, unsafe_allow_html=True)

            for i, lesson_date in enumerate(teaching_dates):
                lesson_num = i + 1
                start_p, end_p = page_plan[i]

                if start_p == "Review":
                    badge = "Review / Marking"
                elif start_p == end_p:
                    badge = f"Page {start_p}"
                else:
                    badge = f"Pages {start_p}–{end_p}"

                st.markdown(f"""
                <div class="lesson-card">
                    <div class="lesson-left">
                        <div class="lesson-title">Lesson {lesson_num}</div>
                        <div class="lesson-date">{lesson_date.strftime('%A, %d %b %Y')}</div>
                    </div>
                    <div class="lesson-badge">{badge}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
