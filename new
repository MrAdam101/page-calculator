import streamlit as st
from datetime import date, timedelta
import math

st.set_page_config(page_title="Book Page Calculator", page_icon="📘", layout="centered")

st.title("📘 Book Page Calculator")
st.write("Calculate how many pages to teach per lesson based on the real class schedule.")

# -----------------------------
# Helper functions
# -----------------------------
def get_teaching_dates(start_date, end_date, selected_days):
    teaching_dates = []
    current = start_date

    while current <= end_date:
        if current.strftime("%A") in selected_days:
            teaching_dates.append(current)
        current += timedelta(days=1)

    return teaching_dates


def split_pages_evenly(total_pages, total_lessons):
    if total_lessons == 0:
        return []

    base_pages = total_pages // total_lessons
    extra_pages = total_pages % total_lessons

    page_plan = []
    current_page = 1

    for i in range(total_lessons):
        pages_this_lesson = base_pages + (1 if i < extra_pages else 0)
        start_page = current_page
        end_page = current_page + pages_this_lesson - 1
        page_plan.append((start_page, end_page))
        current_page = end_page + 1

    return page_plan


# -----------------------------
# Inputs
# -----------------------------
book_name = st.text_input("Book Name", value="Start Right Reader 2")
total_pages = st.number_input("Total Pages", min_value=1, value=60, step=1)

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=date.today())
with col2:
    end_date = st.date_input("End Date", value=date.today() + timedelta(days=30))

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
selected_days = st.multiselect(
    "Teaching Days",
    options=days_of_week,
    default=["Monday", "Wednesday", "Friday"]
)

# -----------------------------
# Calculate
# -----------------------------
if st.button("Calculate Page Plan"):
    if end_date < start_date:
        st.error("End date must be after the start date.")
    elif not selected_days:
        st.error("Please select at least one teaching day.")
    else:
        teaching_dates = get_teaching_dates(start_date, end_date, selected_days)
        total_lessons = len(teaching_dates)

        if total_lessons == 0:
            st.warning("There are no teaching days in that date range.")
        elif total_pages < total_lessons:
            st.warning(
                f"There are {total_lessons} lessons but only {total_pages} pages. "
                f"Some lessons will need to review, combine, or do workbook/checking only."
            )

            # still build a usable plan
            page_plan = []
            current_page = 1
            for i in range(total_lessons):
                if current_page <= total_pages:
                    page_plan.append((current_page, current_page))
                    current_page += 1
                else:
                    page_plan.append(("Review", "Review"))
        else:
            page_plan = split_pages_evenly(total_pages, total_lessons)

        st.subheader("Summary")
        st.write(f"**Book:** {book_name}")
        st.write(f"**Total pages:** {total_pages}")
        st.write(f"**Start date:** {start_date}")
        st.write(f"**End date:** {end_date}")
        st.write(f"**Teaching days:** {', '.join(selected_days)}")
        st.write(f"**Total lessons available:** {total_lessons}")

        if total_lessons > 0:
            avg_pages = total_pages / total_lessons
            st.write(f"**Average pages per lesson:** {avg_pages:.2f}")

        st.subheader("Lesson-by-Lesson Plan")

        for i, lesson_date in enumerate(teaching_dates):
            lesson_num = i + 1
            start_page, end_page = page_plan[i]

            if start_page == "Review":
                st.write(
                    f"**Lesson {lesson_num}** — {lesson_date.strftime('%Y-%m-%d (%A)')}: Review / checking / marking"
                )
            elif start_page == end_page:
                st.write(
                    f"**Lesson {lesson_num}** — {lesson_date.strftime('%Y-%m-%d (%A)')}: Page {start_page}"
                )
            else:
                st.write(
                    f"**Lesson {lesson_num}** — {lesson_date.strftime('%Y-%m-%d (%A)')}: Pages {start_page}–{end_page}"
                )
