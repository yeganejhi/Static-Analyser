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