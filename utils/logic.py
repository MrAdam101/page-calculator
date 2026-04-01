from datetime import timedelta


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
