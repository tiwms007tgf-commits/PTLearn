from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import db, User, Lesson, Quiz, Progress, QuizAttempt, Exercise, ExerciseAttempt
from datetime import datetime
import math
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learning_app.db'
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== AUTH ROUTES ====================

@app.route('/')
def index():
    # Render landing page as the default entry point.
    # Pass `logged_in` so the template can adjust CTA links.
    return render_template('index.html', logged_in=('user_id' in session))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if not username or not password:
            return render_template('register.html', error='Бүх талбарыг бөглөнө үү')

        if password != password_confirm:
            return render_template('register.html', error='Нууц үг таарахгүй байна')

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Хэрэглэгчийн нэр аль хэдийн байна')

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return redirect(url_for('dashboard'))

    return render_template('register.html', hide_sidebar=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))

        return render_template('login.html', error='Буруу мэдээлэл')

    return render_template('login.html', hide_sidebar=True)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


# ==================== MAIN ROUTES ====================

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    lessons = Lesson.query.order_by(Lesson.order).all()

    completed_lessons = Progress.query.filter_by(
        user_id=user.id, completed=True
    ).count()

    total_lessons = len(lessons)
    streak = QuizAttempt.get_streak(user.id)

    current_xp_for_level = int((user.level - 1) ** 2 * 100)
    next_xp_for_level = int(user.level ** 2 * 100)
    xp_progress = user.xp - current_xp_for_level
    xp_needed = next_xp_for_level - current_xp_for_level
    xp_percentage = int((xp_progress / xp_needed) * 100) if xp_needed > 0 else 0

    return render_template('dashboard.html',
        user=user,
        lessons=lessons,
        completed_lessons=completed_lessons,
        total_lessons=total_lessons,
        streak=streak,
        xp_percentage=xp_percentage,
        xp_progress=xp_progress,
        xp_needed=xp_needed
    )


@app.route('/lesson/<int:lesson_id>')
@login_required
def lesson(lesson_id):
    user = User.query.get(session['user_id'])
    lesson = Lesson.query.get(lesson_id)

    if not lesson:
        return redirect(url_for('dashboard'))

    progress = Progress.query.filter_by(
        user_id=user.id,
        lesson_id=lesson_id
    ).first()

    if not progress:
        progress = Progress(user_id=user.id, lesson_id=lesson_id)
        db.session.add(progress)

    if not progress.completed:
        progress.completed = True
        progress.completed_at = datetime.utcnow()
        user.add_xp(25)
        db.session.commit()

    next_lesson = Lesson.query.filter(Lesson.order > lesson.order).order_by(Lesson.order).first()

    return render_template('lesson.html',
        user=user,
        lesson=lesson,
        next_lesson=next_lesson
    )


@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    user = User.query.get(session['user_id'])
    quiz_item = Quiz.query.get(quiz_id)

    if not quiz_item:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        user_answer = request.form.get('answer', type=int)
        is_correct = user_answer == quiz_item.correct_answer

        existing_attempt = QuizAttempt.query.filter_by(
            user_id=user.id,
            quiz_id=quiz_id,
            correct=True
        ).first()

        if is_correct and not existing_attempt:
            user.add_xp(quiz_item.xp_reward)

        attempt = QuizAttempt(
            user_id=user.id,
            quiz_id=quiz_id,
            correct=is_correct
        )
        db.session.add(attempt)
        db.session.commit()

        return jsonify({
            'correct': is_correct,
            'correct_answer': quiz_item.correct_answer,
            'explanation': quiz_item.explanation,
            'xp_earned': quiz_item.xp_reward if (is_correct and not existing_attempt) else 0,
            'user_level': user.level,
            'user_xp': user.xp
        })

    return render_template('quiz.html', user=user, quiz=quiz_item)


@app.route('/code', methods=['GET', 'POST'])
@login_required
def code_lab():
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        code = request.form.get('code', '')
        output = execute_code(code)
        return jsonify({'output': output})

    return render_template('code_lab.html', user=user)


@app.route('/progress')
@login_required
def progress():
    user = User.query.get(session['user_id'])
    lessons = Lesson.query.order_by(Lesson.order).all()

    progress_data = []
    for lesson in lessons:
        p = Progress.query.filter_by(user_id=user.id, lesson_id=lesson.id).first()
        progress_data.append({
            'lesson': lesson,
            'completed': p and p.completed
        })

    return render_template('progress.html', user=user, progress_data=progress_data)


@app.route('/exercises')
@login_required
def exercises():
    user = User.query.get(session['user_id'])
    exercises = Exercise.query.order_by(Exercise.order).all()
    return render_template('exercises.html', user=user, exercises=exercises)


@app.route('/run_exercise', methods=['POST'])
@login_required
def run_exercise():
    user = User.query.get(session['user_id'])
    exercise_id = request.form.get('exercise_id', type=int)
    code = request.form.get('code', '').strip()
    exercise = Exercise.query.get(exercise_id)

    if not exercise:
        return jsonify({'output': 'Алдаа: Дасгал олдсонгүй', 'test_results': [], 'all_passed': False})

    if not code:
        return jsonify({'output': 'Алдаа: Код оруулаагүй байна', 'test_results': [], 'all_passed': False})

    output = execute_code(code)
    test_results = []
    all_passed = True

    for test_case in exercise.test_cases or []:
        expected = test_case.get('expected_output')
        passed = False
        error = None

        if expected is None:
            passed = True
        else:
            passed = output.strip() == str(expected).strip()
            if not passed:
                error = f"Хүлээгдэж буй: {expected}"

        test_results.append({
            'name': test_case.get('name', 'Нэргүй тест'),
            'passed': passed,
            'error': error
        })
        all_passed = all_passed and passed

    attempt = ExerciseAttempt(
        user_id=user.id,
        exercise_id=exercise.id,
        code=code,
        passed=all_passed
    )
    db.session.add(attempt)
    db.session.commit()

    if all_passed and exercise.xp_reward:
        user.add_xp(exercise.xp_reward)
        db.session.commit()

    return jsonify({
        'output': output,
        'test_results': test_results,
        'all_passed': all_passed,
        'xp_earned': exercise.xp_reward if all_passed else 0,
        'user_level': user.level,
        'user_xp': user.xp
    })


# ==================== CODE EXECUTION ====================

def execute_code(code):
    import subprocess
    import signal

    dangerous_keywords = [
        'import os', 'import sys', 'import subprocess',
        '__import__', 'exec', 'eval', '__builtins__'
    ]

    for keyword in dangerous_keywords:
        if keyword in code.lower():
            return f"Алдаа: '{keyword}' ашиглахыг хориглосон (аюулгүй байдлын шалтгаан)."

    try:
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout
        if result.stderr:
            output += '\nАлдаа:\n' + result.stderr

        return output if output else "Код амжилттай ажиллаа (гаралт байхгүй)"

    except subprocess.TimeoutExpired:
        return "Алдаа: Кодын хугацаа хэтэрсэн (>5 секунд). Infinite loop байж магадгүй!"
    except Exception as e:
        return f"Алдаа: {str(e)}"


# ==================== API ROUTES ====================

@app.route('/api/user')
@login_required
def api_user():
    user = User.query.get(session['user_id'])
    return jsonify(user.to_dict())


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    app.logger.warning('404 on %s', request.path)
    return render_template('base.html'), 404


@app.errorhandler(500)
def server_error(error):
    app.logger.exception('500 on %s', request.path)
    return render_template('base.html'), 500


# ==================== DATABASE INITIALIZATION ====================

def seed_exercises():
    if Exercise.query.count() > 0:
        return

    exercises = [
        Exercise(
            title='Сайн байна, Python',
            description='Сайн байна гэж хэвлэх Python програм бич.',
            starter_code='print("Сайн байна, Python!")',
            solution='print("Сайн байна, Python!")',
            test_cases=[
                {'name': 'мэндчилгээ хэвлэх', 'expected_output': 'Сайн байна, Python!'}
            ],
            difficulty='Хялбар',
            xp_reward=10,
            order=1
        ),
        Exercise(
            title='Гурав хүртэл тоол',
            description='1-ээс 3 хүртэл тоонуудыг хэвлэх цикл бич.',
            starter_code='for number in range(1, 4):\n    print(number)',
            solution='for number in range(1, 4):\n    print(number)',
            test_cases=[
                {'name': '1-3 хүртэл хэвлэх', 'expected_output': '1\n2\n3'}
            ],
            difficulty='Хялбар',
            xp_reward=15,
            order=2
        )
        ,
        Exercise(
            title='Нэмэх функц',
            description='2 тоог нэмэх функц бич.',
            starter_code='def add(a, b):\n    # return two numbers sum\n    pass',
            solution='def add(a, b):\n    return a + b',
            test_cases=[
                {'name': '2+3', 'expected_output': '5'},
                {'name': '0+0', 'expected_output': '0'}
            ],
            difficulty='Хялбар',
            xp_reward=12,
            order=3
        ),

        Exercise(
            title='Факториал',
            description='n-ийн факториал олдог функц бич.',
            starter_code='def fact(n):\n    # compute factorial\n    pass',
            solution='def fact(n):\n    res = 1\n    for i in range(1, n+1):\n        res *= i\n    return res',
            test_cases=[
                {'name': 'fact(5)', 'expected_output': '120'},
                {'name': 'fact(0)', 'expected_output': '1'}
            ],
            difficulty='Дунд',
            xp_reward=20,
            order=4
        ),

        Exercise(
            title='List дээр ажиллах',
            description='Өгөгдсөн жагсаалтаас сөрөг утгуудыг салгаж шинэ жагсаалт буцаа.',
            starter_code='def positives(arr):\n    # return positive numbers only\n    pass',
            solution='def positives(arr):\n    return [x for x in arr if x > 0]',
            test_cases=[
                {'name': 'mixed', 'expected_output': '1\n3'},
            ],
            difficulty='Хялбар',
            xp_reward=12,
            order=5
        ),

        Exercise(
            title='Файлын уншилт',
            description='Текст файлын мөрүүдийн тоог буцааг',
            starter_code='def count_lines(path):\n    # return number of lines in file\n    pass',
            solution='def count_lines(path):\n    with open(path, encoding="utf-8") as f:\n        return len(f.readlines())',
            test_cases=[
                {'name': 'file_lines', 'expected_output': '1'}
            ],
            difficulty='Дунд',
            xp_reward=18,
            order=6
        )
    ]

    db.session.add_all(exercises)
    db.session.commit()


with app.app_context():
    db.create_all()
    seed_exercises()

    if Lesson.query.count() == 0:
        try:
            from seed_data import seed_database
            seed_database()
            print("Өгөгдлийн сан амжилттай үүсгэлээ.")
        except Exception as e:
            print("Өгөгдөл үүсгэх амжилтгүй:", e)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)