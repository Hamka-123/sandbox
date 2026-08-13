#Functions in all previous homeworks

def code_page_detector():
    letter = input("Enter a character: ")
    code = ord(letter)
    print("Unicode decimal representation:", code)
    #Define a group of codes by decimal range
    if code < 0 or code > 1535:
        print("Invalid Unicode code point")
    elif code >= 0 and code <= 127: print("EN")        
    elif code >= 1024 and code <= 1279: print("RU")
    elif code >= 1424 and code <= 1535: print("HE")
    else:
        print("Character not in Basic Latin, Cyrillic, or Hebrew ranges")

    #check hex code for utf-8
    hex_code = hex(code)
    print("Unicode hexadecimal representation:", hex_code)
    #Define a group of codes by hex range
    if 0x0000 <= code <= 0x007F:
        print("EN")
    elif 0x0400 <= code <= 0x04FF:
        print("RU")
    elif 0x0590 <= code <= 0x05FF:
        print("HE")
    else:
        print("Character not in Basic Latin, Cyrillic, or Hebrew ranges")

def countdownt_timer():
    from time import sleep
    from datetime import datetime
    import os
    import platform

    stop_time = int(input("Enter stop time in seconds: "))
    '''
    print("before sleep")
    sleep(5)
    print("after sleep")
    '''

    while stop_time > 0:
        print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # Cross-platform beep
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 200)
        elif platform.system() == "Darwin":
            os.system('say "beep"')
        else:
            print('\a')
        print(f"Time left: {stop_time} seconds")
        sleep(1)
        stop_time -= 1
        
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Timer finished!")
    
def html_parser():
    #html text
    html_text = '''
    <h1>Heading1 text</h1>
    <h2>Sub-heading text</h2>
    <p>paragraph 1</p>
    '''
    COLOR_RED = "\033[91m"
    COLOR_YELLOW = "\033[93m"
    COLOR_GREEN = "\033[92m"
    COLOR_RESET = "\033[0m"

    HTML_TAGS = [
        ["h1", COLOR_RED],
        ["h2", COLOR_YELLOW],
        ["p", COLOR_GREEN]
    ]
    result = html_text

    for tag, color in HTML_TAGS:
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        start_index = result.find(start_tag)
        end_index = result.find(end_tag)

        if start_index != -1 and end_index != -1:
            content = result[start_index + len(start_tag):end_index]
            result = result.replace(content, f"{color}{content}{COLOR_RESET}")

    #print colorized html_text to console
    print(result)
    print(type(result))

def print_rectangle():
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
    
def symbol_counter():
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
    
def words_counter():
    # input phrase
    # count, print words number
    # words separators - list
    WORDS_SEPARATORS = [" ", "\n", "!"]

    test_phrase = "Привет! Как дела\n У меня всё хорошо!"

    phrase = input("Введите фразу: ") or test_phrase

    # Заменим все разделители на пробел
    for sep in WORDS_SEPARATORS:
        phrase = phrase.replace(sep, " ")

    # Теперь разбиваем по пробелам и фильтруем пустые строки
    words = [word for word in phrase.split(" ") if word]

    print(f"Количество слов: {len(words)}")


#calling functions
code_page_detector()
countdownt_timer()
html_parser()
print_rectangle()
symbol_counter()
words_counter()