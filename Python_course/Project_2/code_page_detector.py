#input letter
#print codepage

'''
chr(CODE) -> symbol
ord(SYMBOL) -> code

UTF-8 Basic Latin Hex 0x0000-0x007F / Dec 0-127

UTF-8 Hebrew Hex 0x0590-0x05FF / Dec 1424-1535

UTF-8 Cyrillic Hex 0x0400-0x04FF / Dec 1024-1279

'''

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