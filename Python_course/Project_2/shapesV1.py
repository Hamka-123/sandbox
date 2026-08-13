# Calc area, perimeter
# factory function 

import math

def shapes_calc(shape_type):
    
    match shape_type.lower():
        case 's':   
            def squares(side):
                area = side*side
                perimeter = side*4
                return area, perimeter
            return "Square", squares
        
        case 'r':
            def rectangles(width, length):
                area = width * length
                perimeter = (width + length) * 2
                return area, perimeter
            return "Rectangle", rectangles
        
        case 'c':
            def circle(radius):
                PI = math.pi
                area = PI * radius ** 2
                perimeter = 2 * PI * radius
                return area, perimeter
            return "Circle", circle
            
        case 't':
            def triangles(a,b,c):
                pp = (a + b + c) / 2 # Полупериметр
                area = math.sqrt(pp * (pp - a) * (pp - b) * (pp - c))  # Площадь по формуле Герона                                      
                perimeter = a+b+c
                return area, perimeter
            return "Triangle", triangles
        case _: print("Unknown shape type")

def area_perimeter_printer(area, perimeter, name):
    print(f"Shape: {name}")
    print("Area:", area)
    print("Perimeter:", perimeter)
    print("-" * 30)

name, calc_squares = shapes_calc('s')
area_perimeter_printer(*calc_squares(10), name)

name, calc_rectangles = shapes_calc('r')
area_perimeter_printer(*calc_rectangles(10,5), name)

name, calc_circles = shapes_calc('c')
area_perimeter_printer(*calc_circles(5), name)

name, calc_triangles = shapes_calc('t')
area_perimeter_printer(*calc_triangles(2,3,5), name)



