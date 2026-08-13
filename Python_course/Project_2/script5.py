
numbers = [
    [1,2,-33,4],
    [1,2,3,4,22,33,44,-1],
    [1,2,3,4,3,11,-3,987],
]

# find negative, break all
# minimal loops
counter = 0
iterations = 0
for i in numbers:
    if counter > 0:
        break
    for j in i:
        if j < 0:
            print("Found negative:", j)
            counter += 1
            iterations += 1
            break
print("Total iterations:", iterations)


for row in numbers:
    for item in row:
        if item < 0:
            print("Found negative:", item)
            break
    else:
        continue
    break