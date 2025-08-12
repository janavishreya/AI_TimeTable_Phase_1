import random
def optimize_timetable(timetable, input_data):
    """Optimizes timetable to prevent consecutive subjects and maintain balance."""
    for day in timetable:
        subjects = input_data["subjects"]
        for period in range(1, len(timetable[day])):
            if timetable[day][period] == timetable[day][period - 1]:  # Prevent consecutive subjects
                new_subject = random.choice([s for s in subjects if s != timetable[day][period]])
                timetable[day][period] = new_subject
    return timetable
