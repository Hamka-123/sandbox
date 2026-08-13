# text 
phrase = input("Enter a phrase: ")
if not phrase:
    phrase = "Hello world"
# create list:

symbols_counter = [
    ["H",1],
    ["e",1],
    ["e",1],
]
# make the symbol counter
for symbol in phrase:
    found = False
    for i, (s, count) in enumerate(symbols_counter):
        if s == symbol:
            symbols_counter[i][1] += 1
            found = True
            break
    if not found:
        symbols_counter.append([symbol, 1])
        
print(symbols_counter)