# Cinema hall:
'''

3    000101100000110000000000000
2    000000000000000000000000000
1    111111111111111111111111111
    
     _________ SCREEN __________
     
     
Cinema management functions:
- cell ticket
- print cinema hall
- return ticket
- check free places

'''

rows = 10
seats = 15
BG_GREEN = '\033[102m'   # Зеленый фон - Свободно
BG_RED = '\033[101m'     # Красный фон - Занято
BG_RESET = '\033[0m'    # Сброс цвета

hall = [0 for _ in range(rows)]
screen = 'SCREEN'.center(seats * 3 + 7, '=')

def print_cinema_hall(hall, screen):
    """Печатает цветную схему зала с номерами мест"""  
    for i, row_value in enumerate(hall):
        row_num = i + 1
        print(f"Row {row_num:2d}: ", end="")
        for place in range(seats):  # Предполагаем 8 мест в ряду
            if is_seat_celled(row_value, place):
                print(f"{BG_RED}{place+1:2d}{BG_RESET}", end=" ")  # Красный
            else:
                print(f"{BG_GREEN}{place+1:2d}{BG_RESET}", end=" ")  # Зеленый
        print()
        
    print('\n'*1,screen,'\n'*2)

def is_seat_free(row, place):
    """Проверяет свободно ли место (бит = 0)"""
    return (row & (1 << place)) == 0

def is_seat_celled(row, place):
    """Проверяет продано ли место (бит = 1)"""
    return (row & (1 << place)) != 0

def get_free_places(hall):
    """Проверяет свободные места в зале"""
    free_places = {}
    for r, row_value in enumerate(hall, start=1):
        free_in_row = []
        
        for place in range(seats): # Проверяем каждое место в ряду
            if is_seat_free(row_value, place):
                free_in_row.append(place + 1)  # +1 т.к. места с 1
        
        if free_in_row:  # Если есть свободные места в ряду
            free_places[f'Ряд {r}'] = free_in_row
    
    return free_places


def cell_ticket(hall, row, place):
    """Бронирует место (устанавливает бит в 1)"""
    if row < 1 or row > len(hall):
        print(f'Row {row} does not exist')
        return hall
    
    place_index = place - 1  # преобразуем в внутреннее представление
    
    if place_index < 0 or place_index >= seats:
        print(f'Place {place} does not exist')
        return hall
    
    row_index = row - 1  # преобразуем ряд во внутренний индекс
    row_value = hall[row_index]
    
    if is_seat_free(row_value, place_index):
        print(f'Place {place} in row {row} is celled')
        new_hall = hall.copy()
        new_hall[row_index] = row_value | (1 << place_index)
        return new_hall
    else:
        print(f'Place {place} in row {row} is already occupied')
        return hall

def return_ticket(hall, row, place):
    """Освобождает место (устанавливает бит в 0)"""
    if row < 1 or row > len(hall):
        print(f'Row {row} does not exist')
        return hall
        
    place_index = place - 1  # преобразуем в внутреннее представление
    
    if place_index < 0 or place_index >= seats:
        print(f'Place {place} does not exist')
        return hall
        
    row_index = row - 1  # преобразуем ряд во внутренний индекс
    row_value = hall[row_index]
    
    if is_seat_celled(row_value, place_index):
        print(f'Place {place} in row {row} is freed')
        new_hall = hall.copy()
        new_hall[row_index] = row_value & ~(1 << place_index)
        return new_hall
    else:
        print(f'Place {place} in row {row} is already free')
        return hall


#-----------main---------------
print("ПУСТОЙ ЗАЛ:")
print_cinema_hall(hall, screen)

# Тестируем бронирование
print("\n--- БРОНИРУЕМ МЕСТА ---")
hall = cell_ticket(hall, 1, 5)   # Ряд 1, место 5
hall = cell_ticket(hall, 1, 8)   # Ряд 1, место 8
hall = cell_ticket(hall, 3, 12)  # Ряд 3, место 12
hall = cell_ticket(hall, 5, 10)  # Ряд 5, место 10

print("\nЗАЛ ПОСЛЕ БРОНИРОВАНИЯ:")
print_cinema_hall(hall, screen)

# Возвращаем билет
print("\n--- ВОЗВРАЩАЕМ БИЛЕТ ---")
hall = return_ticket(hall, 1, 5)

print("\nЗАЛ ПОСЛЕ ВОЗВРАТА:")
print_cinema_hall(hall, screen)


print("\nБИНОРНОЕ ПРЕДСТАВЛЕНИЕ:")
for i, row in enumerate(hall, start=1):
    binary_row = f'{row:0{seats}b}'
    print(f"Row {i}: {binary_row}")

# Показываем свободные места
free = get_free_places(hall)
print("\nСВОБОДНЫЕ МЕСТА:")
for row, places in free.items():
    print(f"{row}: {places}")

print('------------tests------------')
def show_row_size():
    """Показывает размер ряда в битах"""
    row_value = hall[0]
    binary_representation = f"{row_value:0{seats}b}"
    
    print(f"Количество мест в ряду: {seats}")
    print(f"Битовое представление: {binary_representation}")
    print(f"Длина битовой строки: {len(binary_representation)} бит")
    print(f"Максимальное число, которое можно представить: {2**seats - 1}")

show_row_size()