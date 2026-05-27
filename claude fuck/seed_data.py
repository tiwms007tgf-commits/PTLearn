"""
seed_data.py
Populate database with example lessons, quizzes, and achievements
"""
from app import create_app
from app.database import db
from app.models import Lesson, Quiz, Achievement
import json

lessons_data = [
    {
        'title': 'Python Basics: Variables & Data Types',
        'slug': 'python-basics-variables',
        'description': 'Learn about Python variables and basic data types including strings, integers, floats, and booleans.',
        'content': '''# Python Basics: Variables & Data Types

Variables are containers for storing data values. Python has no command for declaring a variable.

## Variable Names
- Must start with a letter or underscore
- Can contain alphanumeric characters and underscores
- Are case-sensitive

## Data Types
Python has several built-in data types:

### String
Text data enclosed in quotes.

### Integer
Whole numbers without decimals.

### Float
Numbers with decimals.

### Boolean
True or False values.

## Example
```python
name = "Alice"
age = 25
height = 5.6
is_student = True
```

All variables have a type that determines what operations you can perform with them.''',
        'code_example': '''# Variable Assignment
name = "Python Learner"
age = 25
score = 95.5
is_active = True

# Print variables
print(name)
print(age)
print(score)
print(is_active)

# Check types
print(type(name))
print(type(age))
print(type(score))
print(type(is_active))''',
        'difficulty': 1,
        'topic': 'basics',
        'order': 1
    },
    {
        'title': 'String Operations',
        'slug': 'string-operations',
        'description': 'Master string manipulation, concatenation, and formatting in Python.',
        'content': '''# String Operations

Strings are sequences of characters. Python provides many methods for working with strings.

## String Concatenation
Combine strings using the + operator.

## String Formatting
- Using f-strings (Python 3.6+)
- Using .format() method
- Using % operator (legacy)

## String Methods
- .upper() - Convert to uppercase
- .lower() - Convert to lowercase
- .strip() - Remove whitespace
- .replace() - Replace characters
- .split() - Split into list

## Example
```python
name = "Python"
greeting = "Hello, " + name
print(greeting)
```''',
        'code_example': '''# String Concatenation
first = "Hello"
second = "World"
result = first + " " + second
print(result)

# F-strings
name = "Alice"
age = 25
message = f"My name is {name} and I am {age} years old"
print(message)

# String methods
text = "  PYTHON  "
print(text.lower())
print(text.strip())
print(text.replace("PYTHON", "PROGRAMMING"))''',
        'difficulty': 1,
        'topic': 'basics',
        'order': 2
    },
    {
        'title': 'Working with Lists',
        'slug': 'working-with-lists',
        'description': 'Learn how to create, manipulate, and work with lists in Python.',
        'content': '''# Working with Lists

Lists are ordered collections of items that can be changed. They are created using square brackets.

## Creating Lists
```python
numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", 3.14, True]
```

## Accessing List Items
Items are indexed starting from 0. You can also use negative indices.

```python
numbers = [10, 20, 30]
print(numbers[0])  # 10
print(numbers[-1])  # 30
```

## List Methods
- .append() - Add item to end
- .insert() - Add item at position
- .remove() - Remove by value
- .pop() - Remove by index
- .sort() - Sort list
- .reverse() - Reverse list

## List Slicing
Get a portion of a list using slice notation.

```python
numbers = [1, 2, 3, 4, 5]
print(numbers[1:3])  # [2, 3]
print(numbers[:2])   # [1, 2]
print(numbers[2:])   # [3, 4, 5]
```''',
        'code_example': '''# Creating and working with lists
numbers = [1, 2, 3, 4, 5]
print(numbers)
print(numbers[0])
print(numbers[-1])

# List methods
fruits = ["apple", "banana", "cherry"]
fruits.append("date")
print(fruits)

fruits.remove("banana")
print(fruits)

fruits.sort()
print(fruits)

# Slicing
numbers = [10, 20, 30, 40, 50]
print(numbers[1:3])
print(numbers[:2])
print(numbers[2:])''',
        'difficulty': 2,
        'topic': 'data-structures',
        'order': 3
    },
    {
        'title': 'Control Flow: If Statements',
        'slug': 'control-flow-if',
        'description': 'Learn to use conditional statements to control program flow.',
        'content': '''# Control Flow: If Statements

Conditional statements allow your program to make decisions based on conditions.

## If Statement
Executes a block if condition is True.

```python
if age >= 18:
    print("You are an adult")
```

## If-Else Statement
Provides an alternative path when condition is False.

```python
if temperature > 30:
    print("It's hot")
else:
    print("It's not hot")
```

## If-Elif-Else Statement
Test multiple conditions.

```python
score = 85
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("F")
```

## Comparison Operators
- == (equal)
- != (not equal)
- > (greater than)
- < (less than)
- >= (greater than or equal)
- <= (less than or equal)

## Logical Operators
- and (both conditions true)
- or (at least one true)
- not (negates condition)''',
        'code_example': '''# If statement
age = 20
if age >= 18:
    print("You can vote")

# If-else statement
score = 75
if score >= 80:
    print("Pass")
else:
    print("Fail")

# If-elif-else
grade = 85
if grade >= 90:
    print("A")
elif grade >= 80:
    print("B")
elif grade >= 70:
    print("C")
else:
    print("F")

# Logical operators
age = 25
has_license = True
if age >= 18 and has_license:
    print("You can drive")''',
        'difficulty': 2,
        'topic': 'control-flow',
        'order': 4
    },
    {
        'title': 'Loops: For and While',
        'slug': 'loops-for-while',
        'description': 'Master iteration using for and while loops.',
        'content': '''# Loops: For and While

Loops allow you to repeat code blocks.

## For Loop
Iterates over a sequence (list, string, range).

```python
for i in range(5):
    print(i)

for fruit in ["apple", "banana", "cherry"]:
    print(fruit)
```

## While Loop
Repeats as long as condition is True.

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

## Break and Continue
- break: Exit the loop
- continue: Skip to next iteration

```python
for i in range(10):
    if i == 5:
        break
    print(i)

for i in range(10):
    if i % 2 == 0:
        continue
    print(i)  # Prints odd numbers
```

## Nested Loops
Loops inside loops.

```python
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})")
```''',
        'code_example': '''# For loop with range
for i in range(5):
    print(i)

# For loop with list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# While loop
count = 0
while count < 3:
    print(f"Count: {count}")
    count += 1

# Break statement
for i in range(10):
    if i == 5:
        break
    print(i)

# Continue statement
for i in range(5):
    if i == 2:
        continue
    print(i)''',
        'difficulty': 2,
        'topic': 'control-flow',
        'order': 5
    },
    {
        'title': 'Functions: Creating Reusable Code',
        'slug': 'functions-creating-reusable-code',
        'description': 'Learn to write functions to make your code DRY (Don\'t Repeat Yourself).',
        'content': '''# Functions: Creating Reusable Code

Functions are reusable blocks of code that perform specific tasks.

## Defining Functions
```python
def greet(name):
    return f"Hello, {name}!"

message = greet("Alice")
print(message)
```

## Parameters and Arguments
- Parameters: Variables in function definition
- Arguments: Values passed when calling function

```python
def add(a, b):  # a, b are parameters
    return a + b

result = add(5, 3)  # 5, 3 are arguments
```

## Return Values
Functions can return values using the return statement.

```python
def square(x):
    return x * x

print(square(5))  # 25
```

## Default Parameters
Parameters can have default values.

```python
def greet(name="World"):
    return f"Hello, {name}!"

print(greet())  # Hello, World!
print(greet("Alice"))  # Hello, Alice!
```

## Variable Scope
Variables inside functions are local.
Variables outside are global.

```python
x = 10  # Global
def test():
    x = 5  # Local
    print(x)

test()  # Prints 5
print(x)  # Prints 10
```''',
        'code_example': '''# Simple function
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))

# Function with multiple parameters
def add(a, b):
    return a + b

print(add(5, 3))

# Function with default parameter
def power(x, exp=2):
    return x ** exp

print(power(5))     # 25
print(power(5, 3))  # 125

# Function returning multiple values
def get_coordinates():
    return 10, 20

x, y = get_coordinates()
print(f"x={x}, y={y}")

# Recursive function
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120''',
        'difficulty': 3,
        'topic': 'functions',
        'order': 6
    }
]

quizzes_data = [
    {
        'lesson_index': 0,
        'title': 'Variables & Data Types Quiz',
        'description': 'Test your understanding of Python variables and data types.',
        'passing_score': 70,
        'questions': [
            {
                'type': 'multiple_choice',
                'question': 'What will this print?\n\nx = 10\ny = "20"\nprint(type(y))',
                'options': [
                    '<class \'int\'>',
                    '<class \'str\'>',
                    '<class \'float\'>',
                    '<class \'bool\'>'
                ],
                'correct_answer': '<class \'str\'>',
                'explanation': 'y is assigned the string "20", so its type is str (string).'
            },
            {
                'type': 'multiple_choice',
                'question': 'Which of these is a valid variable name?',
                'options': [
                    '123name',
                    'name-var',
                    '_name_var',
                    'class'
                ],
                'correct_answer': '_name_var',
                'explanation': 'Variable names must start with a letter or underscore. _name_var is valid.'
            },
            {
                'type': 'text_input',
                'question': 'What is the type of the value 3.14?',
                'correct_answer': 'float',
                'explanation': 'A number with a decimal point is a float (floating-point number).'
            }
        ]
    },
    {
        'lesson_index': 2,
        'title': 'Lists Quiz',
        'description': 'Test your knowledge of Python lists.',
        'passing_score': 70,
        'questions': [
            {
                'type': 'multiple_choice',
                'question': 'What will be printed?\n\nnums = [1, 2, 3, 4, 5]\nprint(nums[2])',
                'options': [
                    '1',
                    '2',
                    '3',
                    '4'
                ],
                'correct_answer': '3',
                'explanation': 'Lists are zero-indexed. Index 2 refers to the third element, which is 3.'
            },
            {
                'type': 'multiple_choice',
                'question': 'What is the correct way to add an item to the end of a list?',
                'options': [
                    'fruits.add("apple")',
                    'fruits.append("apple")',
                    'fruits.insert("apple")',
                    'fruits.push("apple")'
                ],
                'correct_answer': 'fruits.append("apple")',
                'explanation': 'The append() method adds an item to the end of a list.'
            },
            {
                'type': 'text_input',
                'question': 'What will nums[1:3] return for nums = [10, 20, 30, 40]?',
                'correct_answer': '[20, 30]',
                'explanation': 'Slicing [1:3] returns elements at indices 1 and 2 (not 3).'
            }
        ]
    },
    {
        'lesson_index': 3,
        'title': 'If Statements Quiz',
        'description': 'Test your understanding of conditional statements.',
        'passing_score': 70,
        'questions': [
            {
                'type': 'multiple_choice',
                'question': 'What will be printed?\n\nage = 20\nif age >= 18:\n    print("Adult")\nelse:\n    print("Minor")',
                'options': [
                    'Adult',
                    'Minor',
                    'Nothing',
                    'Error'
                ],
                'correct_answer': 'Adult',
                'explanation': 'age is 20, which is >= 18, so the if block executes.'
            },
            {
                'type': 'multiple_choice',
                'question': 'Which operator means "not equal"?',
                'options': [
                    '!=',
                    '<>',
                    '~=',
                    '!='
                ],
                'correct_answer': '!=',
                'explanation': 'The != operator checks if two values are not equal.'
            }
        ]
    }
]

achievements_data = [
    {
        'slug': 'first_lesson',
        'title': 'First Steps',
        'description': 'Complete your first lesson',
        'icon': '🎯',
        'requirement': 'Complete 1 lesson'
    },
    {
        'slug': 'lesson_master',
        'title': 'Lesson Master',
        'description': 'Complete 10 lessons',
        'icon': '🏆',
        'requirement': 'Complete 10 lessons'
    },
    {
        'slug': 'complete_quiz',
        'title': 'Quiz Taker',
        'description': 'Complete your first quiz',
        'icon': '📝',
        'requirement': 'Complete 1 quiz'
    },
    {
        'slug': 'perfect_quiz',
        'title': 'Perfect Score',
        'description': 'Get 100% on a quiz',
        'icon': '⭐',
        'requirement': 'Score 100% on a quiz'
    },
    {
        'slug': 'level_5',
        'title': 'Rising Star',
        'description': 'Reach Level 5',
        'icon': '🌟',
        'requirement': 'Reach level 5'
    },
    {
        'slug': 'streak_7',
        'title': 'Week Warrior',
        'description': 'Maintain a 7-day streak',
        'icon': '🔥',
        'requirement': 'Maintain 7-day streak'
    },
    {
        'slug': 'level_10',
        'title': 'Expert Developer',
        'description': 'Reach Level 10',
        'icon': '💎',
        'requirement': 'Reach level 10'
    }
]


def seed_database():
    """Seed database with example data"""
    app = create_app('development')
    
    with app.app_context():
        # Check if already seeded
        if Lesson.query.first():
            print('Database already seeded. Skipping...')
            return
        
        print('Seeding database...')
        
        # Create lessons
        print('\nCreating lessons...')
        for idx, lesson_data in enumerate(lessons_data):
            lesson = Lesson(**lesson_data)
            db.session.add(lesson)
            print(f'  ✓ {lesson.title}')
        
        db.session.commit()
        
        # Create quizzes
        print('\nCreating quizzes...')
        lessons = Lesson.query.all()
        for quiz_data in quizzes_data:
            lesson_index = quiz_data.pop('lesson_index')
            quiz_data['lesson_id'] = lessons[lesson_index].id
            quiz_data['questions_json'] = json.dumps(quiz_data.pop('questions'))
            quiz = Quiz(**quiz_data)
            db.session.add(quiz)
            print(f'  ✓ {quiz.title}')
        
        db.session.commit()
        
        # Create achievements
        print('\nCreating achievements...')
        for achievement_data in achievements_data:
            achievement = Achievement(**achievement_data)
            db.session.add(achievement)
            print(f'  ✓ {achievement.title}')
        
        db.session.commit()
        
        print('\n✓ Database seeded successfully!')
        print(f'  - {len(lessons_data)} lessons')
        print(f'  - {len(quizzes_data)} quizzes')
        print(f'  - {len(achievements_data)} achievements')


if __name__ == '__main__':
    seed_database()