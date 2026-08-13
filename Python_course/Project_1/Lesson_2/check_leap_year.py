#Ввести год
#Проверить высокосный он или нет
'''
How to determine whether a year is a leap year
To determine whether a year is a leap year, follow these steps:
1) If the year is evenly divisible by 4, go to step 2. Otherwise, go to step 5.
2) If the year is evenly divisible by 100, go to step 3. Otherwise, go to step 4.
3) If the year is evenly divisible by 400, go to step 4. Otherwise, go to step 5.
4) The year is a leap year (it has 366 days).
5) The year is not a leap year (it has 365 days).
'''
year = int(input("Type the year:\n"))

leap_year = "Год высокосный"
not_leap_year = "Год НЕ высокосный"

if year % 4 == 0: #Step 1
    if year % 100: #Step 2
        if  year % 400: #Step 3
            print(leap_year)
        else: #year == 365 go to Step 5
            print(not_leap_year)
    else: #year == 366 Step 4
        print(leap_year)
else: #year == 365 go to Step 5
   print(not_leap_year)
