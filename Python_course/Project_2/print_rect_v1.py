width = input("Enter width: ")
height = input("Enter height: ")
symbol = input("Enter symbol: ")

# draw rectangle(width, height, symbol)
def draw_rectangle(width, height, symbol):
    for _ in range(height):
        print(symbol * width)
        
draw_rectangle(int(width), int(height), symbol)
print("width:", width)
print("height:", height)
print("symbol:", symbol)
