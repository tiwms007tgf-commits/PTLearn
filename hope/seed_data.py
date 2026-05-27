from app import app, db
from database import User, Lesson, Quiz, Progress
import json

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create lessons
        lessons = [
            Lesson(
                title="Python Basics",
                order=1,
                content="""
                <h3>Welcome to Python!</h3>
                <p>Python is a simple, readable programming language. Let's start with the basics.</p>
                <h4>Variables and Data Types</h4>
                <p>A variable is a container that stores a value. Python has several basic data types:</p>
                <ul>
                    <li><strong>int</strong> - Integer numbers (e.g., 42)</li>
                    <li><strong>float</strong> - Decimal numbers (e.g., 3.14)</li>
                    <li><strong>str</strong> - Text (e.g., "Hello")</li>
                    <li><strong>bool</strong> - True or False</li>
                </ul>
                <p>Variables don't need to be declared with a type; Python figures it out automatically!</p>
                """,
                code_example="""
# Variables in Python
name = "Alice"
age = 25
height = 5.9
is_student = True

print(name)
print(age)
print("I am", height, "feet tall")
                """
            ),
            Lesson(
                title="Loops and Iteration",
                order=2,
                content="""
                <h3>Loops</h3>
                <p>Loops allow you to repeat code multiple times.</p>
                <h4>For Loops</h4>
                <p>Use a <code>for</code> loop to iterate over a sequence:</p>
                <h4>While Loops</h4>
                <p>Use a <code>while</code> loop to repeat while a condition is true.</p>
                """,
                code_example="""
# For loop example
for i in range(5):
    print(i)

# While loop example
count = 0
while count < 3:
    print("Count:", count)
    count += 1
                """
            ),
            Lesson(
                title="Functions",
                order=3,
                content="""
                <h3>Functions</h3>
                <p>Functions are reusable blocks of code. They help organize your program.</p>
                <h4>Defining Functions</h4>
                <p>Use the <code>def</code> keyword to create a function:</p>
                <p>Functions can take parameters and return values.</p>
                """,
                code_example="""
def greet(name):
    return "Hello, " + name

def add(a, b):
    return a + b

print(greet("World"))
print(add(5, 3))
                """
            ),
            Lesson(
                title="Lists and Dictionaries",
                order=4,
                content="""
                <h3>Data Structures</h3>
                <p>Python provides powerful data structures for organizing data.</p>
                <h4>Lists</h4>
                <p>Lists are ordered collections that can contain any type of data.</p>
                <h4>Dictionaries</h4>
                <p>Dictionaries store key-value pairs for quick lookups.</p>
                """,
                code_example="""
# Lists
fruits = ["apple", "banana", "cherry"]
print(fruits[0])
fruits.append("date")

# Dictionaries
person = {
    "name": "Bob",
    "age": 30,
    "city": "NYC"
}
print(person["name"])
                """
            ),
            Lesson(
                title="Conditional Statements",
                order=5,
                content="""
                <h3>Making Decisions with If/Else</h3>
                <p>Conditional statements allow your program to make decisions.</p>
                <h4>If Statements</h4>
                <p>Use <code>if</code>, <code>elif</code>, and <code>else</code> to control program flow based on conditions.</p>
                """,
                code_example="""
age = 20

if age < 13:
    print("Child")
elif age < 18:
    print("Teenager")
else:
    print("Adult")

# Comparison operators
x = 10
if x > 5 and x < 20:
    print("x is between 5 and 20")
                """
            ),
        ]
        
        for lesson in lessons:
            db.session.add(lesson)
        db.session.commit()
        
        # Create quizzes
        quizzes = [
            # Lesson 1 Quizzes
            Quiz(
                lesson_id=1,
                question="What is the correct way to create a variable in Python?",
                options=["x := 5", "x = 5", "var x = 5", "x: 5"],
                correct_answer=1,
                explanation="In Python, we use the = operator to assign values to variables.",
                xp_reward=10,
                order=1
            ),
            Quiz(
                lesson_id=1,
                question="Which data type represents text in Python?",
                options=["int", "str", "float", "bool"],
                correct_answer=1,
                explanation="The str data type represents strings (text) in Python.",
                xp_reward=10,
                order=2
            ),
            Quiz(
                lesson_id=1,
                question="What will print(3 + 4) output?",
                options=["34", "7", "'3 + 4'", "Error"],
                correct_answer=1,
                explanation="Python evaluates 3 + 4 as 7.",
                xp_reward=15,
                order=3
            ),
            # Lesson 2 Quizzes
            Quiz(
                lesson_id=2,
                question="What does range(5) generate?",
                options=["[1, 2, 3, 4, 5]", "[0, 1, 2, 3, 4]", "[1, 2, 3, 4]", "Error"],
                correct_answer=1,
                explanation="range(5) generates numbers from 0 to 4 (5 numbers total, starting at 0).",
                xp_reward=10,
                order=1
            ),
            Quiz(
                lesson_id=2,
                question="Which loop type is best for iterating a set number of times?",
                options=["while loop", "for loop", "do-while loop", "repeat loop"],
                correct_answer=1,
                explanation="for loops are ideal for iterating a known number of times.",
                xp_reward=15,
                order=2
            ),
            # Lesson 3 Quizzes
            Quiz(
                lesson_id=3,
                question="How do you define a function in Python?",
                options=["function myFunc() {}", "def myFunc():", "func myFunc()", "define myFunc()"],
                correct_answer=1,
                explanation="Use the def keyword followed by the function name and parentheses.",
                xp_reward=10,
                order=1
            ),
            Quiz(
                lesson_id=3,
                question="What does a return statement do?",
                options=["Starts the function again", "Sends a value back to the caller", "Prints output", "None of the above"],
                correct_answer=1,
                explanation="return sends a value back from the function to the code that called it.",
                xp_reward=15,
                order=2
            ),
            # Lesson 4 Quizzes
            Quiz(
                lesson_id=4,
                question="How do you access the first element of a list?",
                options=["list[1]", "list[0]", "list.first()", "list(0)"],
                correct_answer=1,
                explanation="Lists in Python use 0-based indexing, so the first element is at index 0.",
                xp_reward=10,
                order=1
            ),
            Quiz(
                lesson_id=4,
                question="What is a dictionary?",
                options=["A list of words", "A key-value data structure", "A sorted list", "An ordered collection"],
                correct_answer=1,
                explanation="Dictionaries store data as key-value pairs for fast lookup.",
                xp_reward=15,
                order=2
            ),
            # Lesson 5 Quizzes
            Quiz(
                lesson_id=5,
                question="What does the 'and' operator do?",
                options=["Adds two numbers", "Returns True if both conditions are True", "Joins two strings", "Creates a list"],
                correct_answer=1,
                explanation="The 'and' operator returns True only if both conditions are True.",
                xp_reward=20,
                order=1
            ),
        ]
        
        for quiz in quizzes:
            db.session.add(quiz)
        db.session.commit()
        
        # Create demo user
        demo_user = User(username="demo")
        demo_user.set_password("demo123")
        demo_user.xp = 150
        demo_user.level = 2
        db.session.add(demo_user)
        db.session.commit()
        
        print("✓ Database seeded successfully!")
        print("Demo user: username='demo', password='demo123'")

if __name__ == '__main__':
    seed_database()