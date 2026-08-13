list1 = [i for i in range(10)]

letter_list = [chr(i) for i in range(97, 123)]

letter_hex_pairs = [[chr(i), hex(i)] for i in range(97, 123)]

numbers = [
           [j**i for j in range(10)] #child lists
           for i in range(10) #parent list
           ]
#print(numbers)

nums = [
    i for i in range(10) if i % 2 == 0
]
print(nums)