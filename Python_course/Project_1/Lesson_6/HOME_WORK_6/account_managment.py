months =    ["January", "February",     "March",    "April",    "May",    "June",     "July",     "August",   "September",    "October", "November", "December" ]
incomes =   [1222,      331,            1456,       177,        81,         991,        661,        6541,       341,            41,         441,        541]
outcomes =   [122,      3331,            56,       17,        81,         991,        661,        6541,       341,            41,         441,        541]


# Print balance for every month
balance = []
for i in range(len(incomes)):
    balance.append(incomes[i]-outcomes[i])
    print(f'Balance of {months[i]} = {balance[i]}')