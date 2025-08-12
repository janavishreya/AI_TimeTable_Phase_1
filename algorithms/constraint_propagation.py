import random
def apply_constraints(timetable, input_data):
    for day in timetable:
        if day in input_data["lab_days"]:
            available_labs = input_data["labs"]
            if available_labs:
                lab_subject = random.choice(available_labs)
                start_period = random.randint(0, len(timetable[day]) - 3)
                timetable[day][start_period:start_period + 3] = [lab_subject] * 3  

    return timetable
