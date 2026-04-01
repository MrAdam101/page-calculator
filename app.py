import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Book Catch-Up Calculator", page_icon="📘", layout="centered")

st.title("📘 Book page Calculator")
st.write("Enter your current page and let the app calculate how many pages you need per lesson to get the book done on time.")

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


def split_remaining_pages(current_page, last_page, total_lessons):
    next_page = current_page + 1
    pages_left = last_page - current_page

    if total_lessons <= 0 or pages_left <= 0:
        return [], pages_left

    base_pages = pages_left // total_lessons
    extra_pages = pages_left % total_lessons

    plan = []
    page_start = next_page

    for i in range(total_lessons):
        pages_this_lesson = base_pages + (1 if i < extra_pages else 0)

        if pages_this_lesson > 0:
            page_end = page_start + pages_this_lesson - 1
            plan.append((page_start, page_end))
            page_start = page_end + 1
        else:
            plan.append(("Review", "Review"))

    return plan, pages_left


# -----------------------------
# Inputs
# -----------------------------
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
    default=["Monday", "Wednesday", "Friday"]
)

# -----------------------------
# Calculate
# -----------------------------
if st.button("Calculate Catch-Up Plan"):
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

            st.subheader("Summary")
            st.write(f"**Book:** {book_name}")
            st.write(f"**Current page completed:** {current_page}")
            st.write(f"**Last page in book:** {last_page}")
            st.write(f"**Pages left:** {pages_left}")
            st.write(f"**Plan from:** {start_date}")
            st.write(f"**End date:** {end_date}")
            st.write(f"**Teaching days:** {', '.join(selected_days)}")
            st.write(f"**Lessons left:** {lessons_left}")
            st.write(f"**Average pages per lesson needed:** {pages_left / lessons_left:.2f}")

            st.subheader("Catch-Up Plan")

            for i, lesson_date in enumerate(teaching_dates):
                lesson_num = i + 1
                start_p, end_p = page_plan[i]

                if start_p == "Review":
                    st.write(
                        f"**Lesson {lesson_num}** — {lesson_date.strftime('%Y-%m-%d (%A)')}: Review / marking"
                    )
                elif start_p == end_p:
                    st.write(
                        f"**Lesson {lesson_num}** — {lesson_date.strftime('%Y-%m-%d (%A)')}: Page {start_p}"
                    )
                else:
                    st.write(
                        f"**Lesson {lesson_num}** — {lesson_date.strftime('%Y-%m-%d (%A)')}: Pages {start_p}–{end_p}"
                    )
