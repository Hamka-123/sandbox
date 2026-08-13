def tri_recursion(k):
  if(k > 0):
    result = k + tri_recursion(k - 1)
    print(result)
  else:
    result = 0
  return result

print("Recursion Example Results:")
tri_recursion(6)

numbers = [6, 5, 4, 3, 2, 1]
summ = 0
for i in numbers:
    summ += i
print(summ)

num = 6
summ = 0
print(f"range: {range(num)}")
for i in range(num+1):
    print(f'f: {i}')
    summ += i
print(summ)