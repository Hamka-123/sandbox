list1 = [
    [1,2,23,3],
    [1,2,23,322,33,55,6],
    [2,333333]
]

def sort2(e):return len(e)
def sort3(e):
    
    return sum(e)

def sort4(e):
    # int("".join(e))
    s = ''
    for i in e:
        s += str(i)
    print(s)
    print(type(s))
    return int(s)


print(min(list1, key=sort4)) # [1, 2, 23, 3]

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def sort1(e):
    # return len(e)
    for i in e:
        result = ord(i)
        
    print(e)
    print(type(e))
    return result


print(min(months, key=sort1))