from console_controls import *
from file_manager import *




# ===== tests =====
#console_controls
print(set_color("sdasdasd", "MAGENTA"))
print(reset_color("nsdbfjb"))
try:
    1 / 0
except Exception as e:
    colorized_exception(e)
    
var = 2
colorized_print(f"test {var}\n","MAGENTA","RED")

colorized_input("Enter your name:", "YELLOW", "black")
print(console_esc_codes.CODES.keys())


#file_manager
print(ddd())




