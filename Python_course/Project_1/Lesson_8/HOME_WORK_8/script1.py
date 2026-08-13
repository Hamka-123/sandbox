# write functions:
'''
- calc_lesson(start_time_string, end_time_string)
- calc_BMI(height, weight, age??)

- users_list = read_users_JSON()

users_list = [
    ["1", "Rosy", "Wileman", "rwileman0@myspace.com", "Female", "17.248.161.92"],
    ["2", "Osgood", "Radden", "oradden1@umich.edu", "Male", "159.227.9.24"],
]
'''
#- calc_lesson(start_time_string, end_time_string)
def calc_lesson(start_time_string, end_time_string):
    from datetime import datetime

    start_time = datetime.strptime(start_time_string, '%H:%M')
    end_time = datetime.strptime(end_time_string, '%H:%M')
    duration = end_time - start_time
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours} hours {minutes} minutes"

#- calc_BMI(height, weight, age??)
def calc_BMI(height, weight):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

#- users_list = read_users_JSON()
def read_users_JSON():
    import json
    import pathlib
    CURRENT_DIR = pathlib.Path(__file__).parent.parent #absolute path to the current directory
    FILE_PATH = CURRENT_DIR.joinpath("JSON_pr1","users.json") #absolute path to the file

    with open(FILE_PATH, 'r') as file:
        users_list = json.load(file)
    return print(type(users_list[::10]))

start_time = "09:00"
end_time = "10:30"
print(calc_lesson(start_time, end_time)) 

height = 170 
weight = 70  
print(calc_BMI(height, weight)) 

users_list = read_users_JSON()
