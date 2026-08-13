#v2
'''
width = 5
height = 4 
border = 2

R - red color background ANSI escape code - border
B - blue color background ANSI escape code - rectangle

'''
width = input("Enter width: ")
height = input("Enter height: ")
border = input("Enter border width: ")

RESET_COLOR = "\033[0m"
RED_COLOR = "\033[41m"  # Red background
BLUE_COLOR = "\033[44m"  # Blue background

def draw_rectangle(width, height, border):
    for i in range(height):
        if i < border or i >= height - border:
            # Верхняя и нижняя граница - полностью красная строка
            print(RED_COLOR + " " * width + RESET_COLOR)
        else:
            # Внутренние строки:
            # левая красная граница + синий заполненный прямоугольник + правая красная граница
            print(
                RED_COLOR + " " * border + RESET_COLOR +                 # левая красная граница
                BLUE_COLOR + " " * (width - 2 * border) + RESET_COLOR +   # синий центр
                RED_COLOR + " " * border + RESET_COLOR                   # правая красная граница
            )

draw_rectangle(int(width), int(height), int(border))
print("width:", width)
print("height:", height)
print("border:", border)
