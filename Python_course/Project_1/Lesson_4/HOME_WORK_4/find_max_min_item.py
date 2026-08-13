# 1 - input comma separated numbers    1,22,-3,44,-3.5 -> string - list method: split()
# 2 - convert to list  [1,22,-3,44,-3.5]  -> list[float]
# find min, max (DO NOT USE STANDART FUNCTIONS min() max())
# print min and max

string = input("Input comma separated numbers (1,22,-3,44,-3.5, etc.):\n")
list = string.split(",")
float_list = [float(x) for x in list]

print(float_list)

min_value = float_list[0]
max_value = float_list[0]
for number in float_list:
    if number > max_value:
        max_value = number
    if number < min_value:
        min_value = number
        
print(f"Maximal number: {max_value}")
print(f"Minimal number: {min_value}")