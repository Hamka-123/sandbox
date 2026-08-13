# input start time
# input end time
# print lesson duration in academic hours (45 min)

start_time = input("Type the start time of lesson in format 'hours:minutes'\n")
end_time = input("Type the end time of lesson in format 'hours:minutes':\n")

start_hours = int(start_time[:2])
start_minutes = int(start_time[3:])
start_all_time_in_minutes = start_hours*60+start_minutes

end_hours = int(end_time[:2])
end_minutes = int(end_time[3:])
end_all_time_in_minutes = end_hours*60+end_minutes

duration_in_minutes = start_all_time_in_minutes - end_all_time_in_minutes
duration_in_academic_hours = duration_in_minutes / 45

print(f"Lesson duration in academic hours: {duration_in_academic_hours:.2f}")