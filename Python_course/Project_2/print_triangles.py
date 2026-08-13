# function print_triangle(h,s)
# function print_triangle(h,s, align)   align: left, center, right
# function print_shapes(h,shape)  # shape: triangle, square, diamond
# while - loop, ask: To print or not to print!!?

'''
    *
  * * *
 * * * *
* * * * *
'''
def print_triangle():
    h = int(input("Enter the height of the triangle: "))
    s = input("Enter the symbol to use: ")
    align = input("Enter alignment (left, center, right): ").lower()
    
    if align == 'left':
        for i in range(1, h + 1):
            print(s * i)
    elif align == 'center':
        for i in range(1, h + 1):
            print((s * i).center(h * 2 - 1))
    elif align == 'right':
        for i in range(1, h + 1):
            print((s * i).rjust(h * 2 - 1))
    else:
        print("Invalid alignment")
        
def print_square():
    size = int(input("Enter the size of the square: "))
    symbol = input("Enter the symbol to use: ")
        
    for _ in range(size):
        print(symbol * size)

def print_diamond():
    size = int(input("Enter the size of the diamond: "))
    symbol = input("Enter the symbol to use: ")

    for i in range(size):
        print(' ' * (size - i - 1) + symbol * (2 * i + 1))
    for i in range(size - 2, -1, -1):
        print(' ' * (size - i - 1) + symbol * (2 * i + 1))


while True:
    input_shape = input("Enter the shape to print (triangle, square, diamond): ").lower()
    if input_shape == "triangle":
        print_triangle()
    elif input_shape == "square":
        print_square()
    elif input_shape == "diamond":
        print_diamond()
    else:
        print("Invalid shape")

    cont = input("Do you want to print another shape? (yes/no): ")
    if cont.lower() != 'yes':
        break