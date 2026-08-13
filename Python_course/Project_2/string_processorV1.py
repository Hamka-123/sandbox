

def string_tranformer(string, worker_function, field_length=20, spacer='.'):
    
    new_string = worker_function(string, field_length, spacer)
    return new_string

'''
str.ljust()
str.rjust()
str.center()
'''


print(string_tranformer('test', str.center)) # -> ........test........
print(string_tranformer('test', str.rjust, field_length=30, spacer='*')) # -> **************************test
print(string_tranformer('test', lambda s,w,spacer: str.center(s,w,spacer).upper(), 50, '_')) # -> _______________________TEST_______________________