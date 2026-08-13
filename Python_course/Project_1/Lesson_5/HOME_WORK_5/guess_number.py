# store secret number 
# user: try to guess

import random

def guess_number(secret_number, attempts):
    while attempts > 0:
        user_number = input(f'''
                            Guess the number (from 1 to 10)
                            You have {attempts} attempts.
                            Your number:
                            ''')
        if not user_number.isdigit():
            print("This is not a number, try again.")
        
        else:
            user_number = int(user_number, 10)
            if not(1 <= user_number <= 10):
                print("Number in wrong range, try again.")
            elif user_number == secret_number:
                print("Yes, that's right. You're a winner! 🎉")
                break
            else:
                print("No, not this number, let's try again")
            
        attempts -= 1
    
    if attempts == 0:
        print("You lost. Better luck next time 🍀")


'''
 #v1 - hard code the number
SECRET_NUMBER = 5
attempts = 10
guess_number(SECRET_NUMBER,attempts)

#v2 - random number in range
secret_number_random = random.randint(1,10)
guess_number(secret_number_random,attempts)
 '''   
version = input("Choose mode (1 = hardcoded, 2 = random): ")

if version == "1":
    guess_number(5, 10)
elif version == "2":
    guess_number(random.randint(1, 10), 10)
else:
    print("Unsupported version.")





    

