# =============================
# Cheat Sheet: try/except in Python
# =============================

#✅TODO: Basic try/except

try:
    x = 1/0
except ZeroDivisionError:
    print("Division by zero!")

#✅TODO: Catch multiple exceptions
 
try:
    y = int("abc")
except (ValueError, TypeError) as e:
    print ("Error:", e)
    
#✅TODO: try/except/else
 
try:
    z = 10/2
except ZeroDivisionError:
    print("Division error")
else:
    print("Everything went fine, result = ", z)

#✅TODO: try/except/finally

try:
    f = open("file.txt", "r")
except FileNotFoundError:
    print("File not found")
finally:
    print("This block always runs")

#✅TODO: Nested try

try:
    print("Outher try")
    try:
        num = int("xyz")
    except ValueError:
        print("Inner try caught ValueError")
except Exception as e:
    print("Outer try caught:", e)


# =============================
# Training Tasks (commented)
# =============================

#✅TODO: 1. Write a try/except that catches ZeroDivisionError when dividing two numbers.
try:
    d = 4/0
except ZeroDivisionError:
    print("Division by zero")

#✅TODO: 2. Write a try/except that handles ValueError when converting input() to int.
try:
    d = int(input("Type something:"))
except ValueError as e:
    print("Error: ", e)
    
#✅TODO: 3. Add an else block that prints "No errors" if no exception occurs.
try:
    d = 2/2
except Exception as e:
    print("Error: ", e)
else: 
    print("All fine")
    
#✅TODO: 4. Add a finally block that always prints "Done".
try:
    d = 4+4
    d == 0
except Exception as e:
    print("Error: ", e)
finally:
    print("Done")
    
#✅TODO: 5. Create a try/except with multiple exception types (ValueError, TypeError).
try:
    d = int("abs")
except (ValueError, TypeError) as e:
    print("Error: ", e)
    
#✅TODO: 6. Make nested try blocks and handle errors in inner and outer separately.
try:
    try:
        d = 1/0
    except ZeroDivisionError:
        print("Division by zero error!")
except Exception as e:
    print("Error: ", e)
    
#✅TODO: 7. Open a non-existing file with try/except and catch FileNotFoundError.
try:
    f = open("file.pdp", "r")
except FileNotFoundError as e:
    print(e)

#✅TODO: 8. Combine try/except/else/finally in one example and explain execution order.
try: #0
    d = int("sdf")
except(ValueError, TypeError) as e:#1
    print(e)
else:#1
    print("ok")
finally:#2
    print("Done")
    
#✅TODO: 9. Write a function that uses try/except to validate integer input from the user.
try:
    data = int(input("Type integer: "))
except (ValueError, TypeError) as e:
    print("Error: ", e)
    
#✅TODO: 10. Write code that raises your own exception (raise ValueError) and handle it.
try:
    raise Exception("CustomError")
except Exception as e:
    print(e)

