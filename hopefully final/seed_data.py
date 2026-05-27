from app import app, db
from database import User, Lesson, Quiz, Progress, Exercise
import json

def seed_database():
    with app.app_context():
        # Existing data устгах
        db.drop_all()
        db.create_all()

        # Хичээлүүд
        lessons = [
            Lesson(
                title="Python-ийн үндэс",
                order=1,
                content="""
                <h3>Python-д тавтай морил!</h3>
                <p>Python бол энгийн бөгөөд уншихад ойлгомжтой програмчлалын хэл юм. Одоо үндсээс нь эхэлье.</p>

                <h4>Хувьсагч болон өгөгдлийн төрлүүд</h4>

                <p>Хувьсагч нь утга хадгалдаг сав юм. Python-д хэд хэдэн үндсэн өгөгдлийн төрөл байдаг:</p>

                <ul>
                    <li><strong>int</strong> - Бүхэл тоо (жишээ нь: 42)</li>
                    <li><strong>float</strong> - Аравтын бутархай тоо (жишээ нь: 3.14)</li>
                    <li><strong>str</strong> - Текст (жишээ нь: "Сайн байна")</li>
                    <li><strong>bool</strong> - Үнэн эсвэл Худал</li>
                </ul>

                <p>Python-д хувьсагчийн төрлийг урьдчилж зарлах шаардлагагүй. Python өөрөө автоматаар тодорхойлдог.</p>
                """,
                code_example="""
# Python дахь хувьсагчид
name = "Alice"
age = 25
height = 5.9
is_student = True

print(name)
print(age)
print("Миний өндөр", height, "фут")
                """
            ),

            Lesson(
                title="Давталт ба Loop",
                order=2,
                content="""
                <h3>Loop</h3>

                <p>Loop нь кодыг олон дахин ажиллуулах боломж олгодог.</p>

                <h4>For Loop</h4>

                <p><code>for</code> loop нь дараалсан өгөгдлүүдээр давтахад ашиглагддаг.</p>

                <h4>While Loop</h4>

                <p><code>while</code> loop нь нөхцөл үнэн байх хугацаанд давтагдана.</p>
                """,
                code_example="""
# For loop жишээ
for i in range(5):
    print(i)

# While loop жишээ
count = 0

while count < 3:
    print("Тоололт:", count)
    count += 1
                """
            ),

            Lesson(
                title="Функцүүд",
                order=3,
                content="""
                <h3>Функцүүд</h3>

                <p>Функц нь дахин ашиглаж болох кодын хэсэг юм. Энэ нь програмыг эмх цэгцтэй болгодог.</p>

                <h4>Функц тодорхойлох</h4>

                <p>Функц үүсгэхдээ <code>def</code> түлхүүр үгийг ашиглана.</p>

                <p>Функц нь параметр авч мөн утга буцааж чадна.</p>
                """,
                code_example="""
def greet(name):
    return "Сайн байна, " + name

def add(a, b):
    return a + b

print(greet("Дэлхий"))
print(add(5, 3))
                """
            ),

            Lesson(
                title="Жагсаалт ба Dictionary",
                order=4,
                content="""
                <h3>Өгөгдлийн бүтэц</h3>

                <p>Python нь өгөгдөл зохион байгуулах хүчирхэг бүтэцтэй.</p>

                <h4>Жагсаалт (List)</h4>

                <p>List нь ямар ч төрлийн өгөгдөл хадгалж болох дараалсан цуглуулга юм.</p>

                <h4>Dictionary</h4>

                <p>Dictionary нь түлхүүр-утгын хосоор өгөгдөл хадгалдаг.</p>
                """,
                code_example="""
# Жагсаалт
fruits = ["алим", "банана", "интоор"]

print(fruits[0])

fruits.append("гүзээлзгэнэ")

# Dictionary
person = {
    "name": "Боб",
    "age": 30,
    "city": "УБ"
}

print(person["name"])
                """
            ),

            Lesson(
                title="Нөхцөлт өгүүлбэр",
                order=5,
                content="""
                <h3>If/Else ашиглан шийдвэр гаргах</h3>

                <p>Нөхцөлт өгүүлбэр нь програмд шийдвэр гаргах боломж олгодог.</p>

                <h4>If Statement</h4>

                <p><code>if</code>, <code>elif</code>, болон <code>else</code> ашиглан нөхцөлөөс хамаарч код ажиллуулна.</p>
                """,
                code_example="""
age = 20

if age < 13:
    print("Хүүхэд")

elif age < 18:
    print("Өсвөр нас")

else:
    print("Насанд хүрсэн")

# Харьцуулах операторууд
x = 10

if x > 5 and x < 20:
    print("x нь 5 болон 20-ын хооронд байна")
                """
            ),
            Lesson(
                title="Текст болон String",
                order=6,
                content="""
                <h3>String буюу текст</h3>
                <p>String нь текстийг илэрхийлнэ. Үндсэн функцууд: concatenation, slicing, форматлах.</p>
                """,
                code_example='''
# Strings
greet = "Hello"
name = "Дэлхий"
print(greet + ", " + name)
print(f"{name} - {len(name)} тэмдэгт")
'''
            ),

            Lesson(
                title="Файлын удирдлага",
                order=7,
                content="""
                <h3>Файлын уншлага, бичлэг</h3>
                <p>open(), read(), write() ашиглан файлыг удирдана.</p>
                """,
                code_example='''
# File I/O
with open('hello.txt', 'w', encoding='utf-8') as f:
    f.write('Сайн байна, Файл!')
with open('hello.txt', 'r', encoding='utf-8') as f:
    print(f.read())
'''
            ),

            Lesson(
                title="Модуль ба Сан",
                order=8,
                content="""
                <h3>Модуль, пакет</h3>
                <p>Python кодыг дахин ашиглахын тулд модулиуд, пакетууд ашиглана.</p>
                """,
                code_example='''
# Import example
import math
print(math.sqrt(16))
'''
            ),

            Lesson(
                title="Алдаа удирдах (Exceptions)",
                order=9,
                content="""
                <h3>Exception handle</h3>
                <p>try/except ашиглан алдааг барьж авах.</p>
                """,
                code_example='''
try:
    x = int('abc')
except ValueError:
    print('Тоог хөрвүүлэх боломжгүй')
'''
            ),

            Lesson(
                title="Обьект чиглэсэн програмчлал (OOP)",
                order=10,
                content="""
                <h3>Класс ба объекt</h3>
                <p>Класс нь объект үүсгэх загвар юм.</p>
                """,
                code_example='''
class Person:
    def __init__(self, name):
        self.name = name
    def greet(self):
        return f"Сайн байнa, {self.name}"

p = Person('Алекс')
print(p.greet())
'''
            ),

            Lesson(
                title="List comprehension",
                order=11,
                content="""
                <h3>List comprehension</h3>
                <p>Цэвэр бөгөөд богиногоор list үүсгэх арга.</p>
                """,
                code_example='''
squares = [x*x for x in range(6)]
print(squares)
'''
            ),

            Lesson(
                title="Lambda болон Higher-order функцууд",
                order=12,
                content="""
                <h3>Lambda, map, filter</h3>
                <p>Жижиг функцуудыг нэг мөрөөр тодорхойлно.</p>
                """,
                code_example='''
add = lambda a, b: a + b
print(add(2,3))
print(list(map(lambda x: x*2, [1,2,3])))
'''
            ),

            Lesson(
                title="Стандарт сан (Standard Library)",
                order=13,
                content="""
                <h3>Стандарт сангууд</h3>
                <p>datetime, json, random зэрэг хүчирхэг сангуудтай танилц.</p>
                """,
                code_example='''
import datetime
print(datetime.datetime.utcnow())
'''
            ),

            Lesson(
                title="Багц ба виртуал орчин",
                order=14,
                content="""
                <h3>pip, виртуал орчин</h3>
                <p>pip ашиглан сан суулгаж, virtualenv ашиглан тусгаарлах.</p>
                """,
                code_example='''
# pip install example: pip install flask
'''
            ),

            Lesson(
                title="Тест ба Debug хийх",
                order=15,
                content="""
                <h3>Unit тест, Debug</h3>
                <p>pytest, print debugging болон pdb ашиглахад хялбар.</p>
                """,
                code_example='''
def add(a,b):
    return a+b

assert add(2,3) == 5
'''
            ),
        ]

        for lesson in lessons:
            db.session.add(lesson)

        db.session.commit()

        # Quiz-үүд
        quizzes = [

            # Lesson 1
            Quiz(
                lesson_id=1,
                question="Python-д хувьсагч үүсгэх зөв арга аль нь вэ?",
                options=["x := 5", "x = 5", "var x = 5", "x: 5"],
                correct_answer=1,
                explanation="Python-д хувьсагчид утга оноохдоо = оператор ашигладаг.",
                xp_reward=10,
                order=1
            ),

            Quiz(
                lesson_id=1,
                question="Python-д текстийг ямар өгөгдлийн төрөл илэрхийлдэг вэ?",
                options=["int", "str", "float", "bool"],
                correct_answer=1,
                explanation="str төрөл нь текст буюу string хадгалдаг.",
                xp_reward=10,
                order=2
            ),

            Quiz(
                lesson_id=1,
                question="print(3 + 4) ямар үр дүн хэвлэх вэ?",
                options=["34", "7", "'3 + 4'", "Алдаа"],
                correct_answer=1,
                explanation="Python 3 + 4-г тооцоолж 7 болгодог.",
                xp_reward=15,
                order=3
            ),

            # Lesson 2
            Quiz(
                lesson_id=2,
                question="range(5) юу үүсгэдэг вэ?",
                options=["[1, 2, 3, 4, 5]", "[0, 1, 2, 3, 4]", "[1, 2, 3, 4]", "Алдаа"],
                correct_answer=1,
                explanation="range(5) нь 0-ээс 4 хүртэлх 5 тоо үүсгэнэ.",
                xp_reward=10,
                order=1
            ),

            Quiz(
                lesson_id=2,
                question="Тодорхой тооны давталт хийхэд аль loop хамгийн тохиромжтой вэ?",
                options=["while loop", "for loop", "do-while loop", "repeat loop"],
                correct_answer=1,
                explanation="for loop нь тодорхой тооны давталтад хамгийн тохиромжтой.",
                xp_reward=15,
                order=2
            ),

            # Lesson 3
            Quiz(
                lesson_id=3,
                question="Python-д функцыг хэрхэн тодорхойлдог вэ?",
                options=["function myFunc() {}", "def myFunc():", "func myFunc()", "define myFunc()"],
                correct_answer=1,
                explanation="def түлхүүр үгийг ашиглан функц үүсгэдэг.",
                xp_reward=10,
                order=1
            ),

            Quiz(
                lesson_id=3,
                question="return statement юу хийдэг вэ?",
                options=[
                    "Функцыг дахин эхлүүлдэг",
                    "Утгыг дуудаж буй код руу буцаадаг",
                    "Текст хэвлэдэг",
                    "Дээрх бүгд биш"
                ],
                correct_answer=1,
                explanation="return нь функцээс утга буцаадаг.",
                xp_reward=15,
                order=2
            ),

            # Lesson 4
            Quiz(
                lesson_id=4,
                question="Жагсаалтын эхний элементийг хэрхэн авах вэ?",
                options=["list[1]", "list[0]", "list.first()", "list(0)"],
                correct_answer=1,
                explanation="Python list нь 0-с эхэлдэг index ашигладаг.",
                xp_reward=10,
                order=1
            ),

            Quiz(
                lesson_id=4,
                question="Dictionary гэж юу вэ?",
                options=[
                    "Үгсийн жагсаалт",
                    "Түлхүүр-утгын бүтэц",
                    "Эрэмбэлсэн жагсаалт",
                    "Дараалсан цуглуулга"
                ],
                correct_answer=1,
                explanation="Dictionary нь өгөгдлийг түлхүүр-утгын хосоор хадгалдаг.",
                xp_reward=15,
                order=2
            ),

            # Lesson 5
            Quiz(
                lesson_id=5,
                question="'and' оператор юу хийдэг вэ?",
                options=[
                    "Хоёр тоог нэмдэг",
                    "Хоёр нөхцөл хоёулаа үнэн үед True буцаадаг",
                    "Хоёр string нийлүүлдэг",
                    "List үүсгэдэг"
                ],
                correct_answer=1,
                explanation="'and' оператор нь хоёр нөхцөл хоёулаа үнэн үед True болдог.",
                xp_reward=20,
                order=1
            ),
            # Lesson 6
            Quiz(
                lesson_id=6,
                question="String-ийг хэрхэн уртасгах вэ?",
                options=["s1 + s2", "s1 - s2", "s1.append(s2)", "concat(s1,s2)"],
                correct_answer=0,
                explanation="Python-д strings-г + оператороор нийлүүлдэг.",
                xp_reward=10,
                order=1
            ),

            # Lesson 7
            Quiz(
                lesson_id=7,
                question="Файлыг бичихэд ашигладаг режим аль вэ?",
                options=["'r'", "'w'", "'x'", "'a'"],
                correct_answer=1,
                explanation="'w' нь бичих горим бөгөөд файл байхгүй бол үүсгэнэ.",
                xp_reward=10,
                order=1
            ),

            # Lesson 8
            Quiz(
                lesson_id=8,
                question="math.sqrt(9) ямар утга буцаах вэ?",
                options=["3", "9", "81", "Алдаа"],
                correct_answer=0,
                explanation="sqrt(9) нь 3-ыг буцаана.",
                xp_reward=10,
                order=1
            ),

            # Lesson 9
            Quiz(
                lesson_id=9,
                question="Алдааг барихад ямар блок ашигладаг вэ?",
                options=["try/except", "if/else", "for/while", "with/open"],
                correct_answer=0,
                explanation="try/except нь exception-үүдийг барьдаг.",
                xp_reward=10,
                order=1
            ),

            # Lesson 10
            Quiz(
                lesson_id=10,
                question="Класс-д __init__ ямар зориулалттай вэ?",
                options=["Обьект үүсгэх", "Анхны тохиргоог (constructor) хийх", "Функц дуудна", "Мэдээлэл хэвлэх"],
                correct_answer=1,
                explanation="__init__ нь объект үүсэх үед анхны тохиргоог гүйцэтгэнэ.",
                xp_reward=15,
                order=1
            ),

            # Lesson 11
            Quiz(
                lesson_id=11,
                question="List comprehension ашиглан 0-4 квадратуудыг үүсгэх код?",
                options=["[x for x in range(5)]", "[x*x for x in range(5)]", "list(range(5))", "map(x*x, range(5))"],
                correct_answer=1,
                explanation="[x*x for x in range(5)] нь квадратыг үүсгэнэ.",
                xp_reward=10,
                order=1
            ),

            # Lesson 12
            Quiz(
                lesson_id=12,
                question="Lambda функц ямар нөхцөлд ашиглагддаг вэ?",
                options=["Том функц бичихэд", "Нэг мөрийн жижиг функц хэрэглэхэд", "Файл уншихад", "Класс үүсгэхэд"],
                correct_answer=1,
                explanation="Lambda нь богино нэг мөрийн функцыг тодорхойлоход ашиглагддаг.",
                xp_reward=10,
                order=1
            ),

            # Lesson 13
            Quiz(
                lesson_id=13,
                question="datetime.datetime.utcnow() юу буцаана?",
                options=["Одоо цаг (UTC)", "Хоногийн тоо", "Текст мөр", "Алдаа"],
                correct_answer=0,
                explanation="utcnow() нь одоогийн UTC цагийг буцаана.",
                xp_reward=10,
                order=1
            ),

            # Lesson 14
            Quiz(
                lesson_id=14,
                question="pip ашигладаг гол зорилго юу вэ?",
                options=["Код бичих", "Сан суулгах", "Файлыг унших", "Тест ажиллуулах"],
                correct_answer=1,
                explanation="pip нь Python сан (package) суулгахад ашиглагддаг.",
                xp_reward=10,
                order=1
            ),

            # Lesson 15
            Quiz(
                lesson_id=15,
                question="Unit тестэнд assert ашиглахад ямар давуу талтай вэ?",
                options=["Кодыг хурдан ажиллуулна", "Функц бүр зөв ажиллаж байгааг шалгах", "Файлыг устгана", "Debug хийхгүй"],
                correct_answer=1,
                explanation="assert-ууд нь функцийн гаралт зөв эсэхийг шалгана.",
                xp_reward=15,
                order=1
            ),
        ]

        for quiz in quizzes:
            db.session.add(quiz)

        db.session.commit()

        # Exercises (also seed some beginner exercises)
        exercises = [
            Exercise(
                title='Сайн байна, Python',
                description='Сайн байна гэж хэвлэх Python програм бич.',
                starter_code='print("Сайн байна, Python!")',
                solution='print("Сайн байна, Python!")',
                test_cases=[{'name': 'мэндчилгээ хэвлэх', 'expected_output': 'Сайн байна, Python!'}],
                difficulty='Хялбар',
                xp_reward=10,
                order=1
            ),
            Exercise(
                title='Гурав хүртэл тоол',
                description='1-ээс 3 хүртэл тоонуудыг хэвлэх цикл бич.',
                starter_code='for number in range(1, 4):\n    print(number)',
                solution='for number in range(1, 4):\n    print(number)',
                test_cases=[{'name': '1-3 хүртэл хэвлэх', 'expected_output': '1\n2\n3'}],
                difficulty='Хялбар',
                xp_reward=15,
                order=2
            ),
            Exercise(
                title='Нэмэх функц',
                description='2 тоог нэмэх функц бич.',
                starter_code='def add(a, b):\n    # return two numbers sum\n    pass',
                solution='def add(a, b):\n    return a + b',
                test_cases=[{'name': '2+3', 'expected_output': '5'}],
                difficulty='Хялбар',
                xp_reward=12,
                order=3
            ),
        ]

        db.session.add_all(exercises)
        db.session.commit()

        # Demo хэрэглэгч
        demo_user = User(username="demo")
        demo_user.set_password("demo123")
        demo_user.xp = 150
        demo_user.level = 2

        db.session.add(demo_user)
        db.session.commit()

        print("✓ Өгөгдлийн сан амжилттай үүслээ!")
        print("Demo хэрэглэгч: username='demo', password='demo123'")


if __name__ == '__main__':
    seed_database()