import random
def resolve_conflicts(timetable, input_data):
    """Fixes any remaining conflicts ensuring no free periods."""
    for day in timetable:
        for period in range(len(timetable[day])):
            if timetable[day][period] is None:  # Fill empty periods
                timetable[day][period] = random.choice(input_data["subjects"])

    return timetable
