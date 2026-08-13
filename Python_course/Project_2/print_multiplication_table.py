# input max number
# create tuple (comprehension)
# print table to console
max_number = int(input("Enter a number: "))

multiplication_table = tuple(f'{i} * {j} = {i*j}' for i in range(1, max_number + 1) for j in range(1, max_number + 1))

center = int(max_number / 2)


for i in range(max_number): #row
    row1 = multiplication_table[0:center+1]
    print(row1)
    row2 = multiplication_table[center+2:]
    print(row2)

'''
for entry in multiplication_table:
    print(f"{entry[0]} x {entry[1]} = {entry[2]}")
    if entry[0] == 1:
        print("\n")
''' 
    
#TODO: pretify print