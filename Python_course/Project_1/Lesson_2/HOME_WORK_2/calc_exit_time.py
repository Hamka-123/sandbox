# input flight time
# input time to airoport 
# security check time (3 hours)
# print home exit time

closed_gate_time = input("When gate will be closed?\n(Hours:Minutes)")
time_to_airport = input("How much time you ride to airport\n(Hours:Minutes)")
time_to_security_check = input("How much time you need for security check and registration? (Usually it 3-4 hours before gate closed)\n(Hours)")


closed_gate_hours = int(closed_gate_time.split(":")[0])
closed_gate_minutes = int(closed_gate_time.split(":")[1])
closed_gate_all_time_in_minutes = closed_gate_hours*60+closed_gate_minutes

time_to_airport_hours = int(time_to_airport.split(":")[0])
time_to_airport_minutes = int(time_to_airport.split(":")[1])
airport_all_time_in_minutes = time_to_airport_hours*60+time_to_airport_minutes

time_to_security_check_hours = int(time_to_security_check)
security_check_all_time_in_minutes = time_to_security_check_hours*60



home_exit_time = (closed_gate_all_time_in_minutes - security_check_all_time_in_minutes - airport_all_time_in_minutes) / 60
hours = int(home_exit_time)
minutes = int((home_exit_time - hours) * 60)

formatted_time = f"{hours:02}:{minutes:02}"
print(f"You must start at {formatted_time}")
