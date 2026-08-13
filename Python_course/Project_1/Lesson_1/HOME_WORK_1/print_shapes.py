# Print to console
# rectangles
'''
********
********
********


. . . . . . . 
. . . . . . . 
. . . . . . . 

# print flag
# USA flag

'''
# Printing to console rectangle
height, width = 5, 10
dots_symbol = " . "
for _ in range(height):
    print(dots_symbol*width)


#Printing to console triangle
height = 10  # triangle height
for i in range(0, height + 1):
    spaces = " " * (height - i)  # Count spaces for left
    stars = "*" * (2 * i - 1)  # Count of stars (+2 for every row)
    print(spaces + stars)


#Printing to console circle
width = 50
circle = [
    "       *****       ",
    "    **       **    ",
    "  **           **  ",
    " **             ** ",
    " **             ** ",
    " **             ** ",
    "  **           **  ",
    "    **       **    ",
    "       *****       "
]
for row in circle:
    print(row)
# P.S. Maybe I can calculate center of circle and automatically draw the circle, 
# but it was not in task and nobody will pay me for it ;)


# Printing to console two-color flag
first_color, second_color = "/", "D"
height, width = 6, 20

for _ in range(height//2):
    print(first_color*width)
for _ in range(height//2):
    print(second_color*width)


# Printing to console USA flag
stars = "★"
even_stars = (" " + stars) * 8
odd_stars = (stars + " ") * 9
rows = 14
red_line = "/"
white_line = "="

i = 0
while i < rows/2: #part with stars
    if i % 2 == 1: #if row odd
        print(odd_stars + red_line*32)
        i +=1
    if i % 2 == 0: #if row even
        print(even_stars + "  "+ white_line*32)
        i +=1
i = 0
while i < rows/2: #part with only lines
    if i % 2 == 1: #if row odd
        print(white_line*50)
        i +=1
    if i % 2 == 0: #if row even
        print(red_line*50)
        i +=1

#Printing to console Israel flag
'''
- you can configure it if you would like drawing with colored hearts or simple chars
- use True in var 'draw_with_hearts' for colored hearts (blue for lines and red for David's star)
- use False in var 'draw_with_hearts' for simple chars and write what char you want 
for 'line_symbol' and 'star_symbol' and 'background_symbol' at the start of program
'''
width = back_width = 50
background_symbol = " "
line_symbol = "1"
star_symbol = "0"

draw_with_hearts = True # True/False - to select draw hearts or simple chars

if draw_with_hearts:
    width = width // 2 #because hearts have 2 symbols
    back_width = width *2
    line_symbol = "\U0001F499" #Blue hearth
    star_symbol = "\U0001F499"#"\u2764\uFE0F" #Red hearth
    star = [ 
    "       *      ",
    "      **      ",
    "********     ",
    "   **      **    ",
    "   *        *   ",
    "   **      **    ",
    "********     ",
    "      **      ",
    "       *      ",
]
else:
    star = [
    "       *       ",
    "      * *      ",
    "* * * * * * * *",
    " * *       * * ",
    "  *         *  ",
    " * *       * * ",
    "* * * * * * * *",
    "      * *      ",
    "       *       ",
]
# P.S. If i will pay more time, possible automatically calculate 
# the position of character anf draw the David's star without massive of chars
# Bonus: let's find bug =)

print(background_symbol * back_width) # Top part of white background
    
for _ in range(2): # Top blue line
    print(line_symbol * width)

print(background_symbol * back_width) # Top-center part of white background

for line in star: # David's star
    line = line.replace(" ", background_symbol).replace("*", star_symbol) #replace background and lines in star to specified
    if draw_with_hearts:
        line = line.center(width*2, background_symbol)
        print(line) #print star at the center and fill background around
    else:
        print(line.center(width, background_symbol)) #print star at the center and fill background around   

print(background_symbol * back_width) # Bottom-center part of white background

for _ in range(2): # Bottom blue line
    print(line_symbol * width)

print(background_symbol * back_width) # Bottom part of white background