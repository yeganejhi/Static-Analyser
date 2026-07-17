# sample_code.py
def greet(name):
    message = "Hello" + name
    temp_data = 42
    print(message)
    return message

greet("Alicia")

def calculateScore(user_id):
    temp_score = 100
    return temp_score

class student_info:
    def __init__(self):
        self.age = 20

class ValidClass:
    def correct_function(self):
        pass

def check_status(score):
    if score > 50:
        return "Pass"
    else:
        raise ValueError("Failed")
    
    print("This will never print!")
    x = 10

def check_logic(x, y):
    if x > 10 and y < 5: 
        for i in range(5):
            print(i)
    return x

def super_complex_function(a, b, c):
    if a > 10 and b < 5:
        if c == 0:
            for i in range(10):
                if i % 2 == 0:
                    print("Even")
        else:
            while b < 10:
                b += 1
    elif a == 5 or b == 5:
        if c > 10:
            return True
    else:
        for j in range(5):
            print(j)
    return False

def test_function_with_if_else_return():
    if True:
        return 1
    else:
        return 2
    print("This is dead too!")


def security_test():
    user_input = "print('hacked!')"
    eval(user_input)  
    exec(user_input)  
    
    query = "SELECT * FROM users WHERE id = " + user_input

def performance_test():
    result = ""
    for i in range(1000):
        result = result + str(i)  
    return result

def infinite_loop_test():
    while True:  
        print("This will run forever!")

def good_performance():
    parts = []
    for i in range(1000):
        parts.append(str(i))
    return "".join(parts)

def safe_function():
    x = 10
    y = 20
    return x + y

def complex_but_ok():
    result = 0
    for i in range(10):
        if i % 2 == 0:
            result += i
        else:
            result -= i
    return result