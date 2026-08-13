import time


html_text_0 = '''
<h1>Heading1 
<p>inside paragraph 
<b>and bold</b>
</p> after p
</h1>
<p>paragraph 
<b>and bold</b>
</p>
'''
html_text = '''
<h1>Heading1 text</h1>
<h2>Sub-heading text</h2>
<p>paragraph 1</p>
'''
# Цвета для текста
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"

# Сопоставление тегов с цветами
HTML_TAGS = {
    "h1": COLOR_RED,
    "h2": COLOR_YELLOW,
    "p": COLOR_GREEN,
    "b": COLOR_BLUE,
}

def parse_html(text, i=0, stack=None):
    if stack is None:
        stack = []

    result = ""
    while i < len(text):
        if text[i] == "<":
            j = text.find(">", i)
            tag_content = text[i+1:j].strip()
            is_closing = tag_content.startswith("/")

            if is_closing:
                # закрывающий тег -> выходим из рекурсии
                return result, j + 1
            else:
                # открывающий тег
                tag = tag_content.split()[0]   # берём только имя тега
                stack.append(tag)
                inner, new_i = parse_html(text, j + 1, stack)
                color = HTML_TAGS.get(tag, "")
                reset = COLOR_RESET if color else ""
                result += f"{color}{inner}{reset}"
                stack.pop()
                i = new_i
                continue
        else:
            if stack:
                color = HTML_TAGS.get(stack[-1], "")
                reset = COLOR_RESET if color else ""
                result += f"{color}{text[i]}{reset}"
            else:
                result += text[i]
            i += 1
    return result, i

#measure the time
start_time = time.time()
colored_text, _ = parse_html(html_text)
end_time = time.time()

print(colored_text)
print(f"Parsing time: {end_time - start_time:.6f} seconds")
