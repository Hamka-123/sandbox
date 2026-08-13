

def handler_creator(key_code):
    event = ''
    def handler():
        nonlocal event
        button = input("Press any button: ")
        if ord(button) == key_code:
            if key_code == 32:
                event = "Space pressed"
            elif key_code == 46:
                event = "Dot pressed"
            elif key_code == 127:
                event = "Delete pressed"
            print(event)
        else:
            print(f"Pressed key code = {ord(button)}")
    return handler

space_button_handler = handler_creator(32)
dot_button_handler = handler_creator(46)
del_button_handler = handler_creator(127)

space_button_handler() 
dot_button_handler()
del_button_handler()