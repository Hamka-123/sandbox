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
