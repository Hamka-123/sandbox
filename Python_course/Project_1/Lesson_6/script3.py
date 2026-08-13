numbers = [11, 2, 3444, -4, 44, -33]

# find minimum

min = numbers[0]
max = numbers[0]

for number in numbers:
    if number < min:
        min = number
        pass
    if number > max:
        max = number
        pass

    pass

#print(f'max = {max} min = {min}')


months =    ["January", "February",     "March", "April", "May",    "June",     "July",     "August",   "September",    "October", "November", "December" ]
incomes =   [1222,          331,        1456,       177,    81,     991,        661,        6541,       341,            41,         441,        541]

# print month name with min income
min_income = incomes[0]
index_months = 0

for income in incomes:
    if income < min_income:
        min_income = income
        index_months = incomes.index(income)
        
print(f'Month name with min income:  {months[index_months]}')

#v2
months_v2 =    ["January", "February",     "March", "April", "May",    "June",     "July",     "August",   "September",    "October", "November", "December" ]
incomes_v2 =   [1222,          331,        1456,       177,    81,     991,        661,        6541,       341,            41,         441,        541]

months_v2_sorted, incomes_v2_sorted = zip(*sorted(zip(months_v2, incomes_v2), key=lambda x: x[1]))

print(f'Month name with min income:  {months_v2_sorted[0]}')




        

