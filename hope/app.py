from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import db, User, Lesson, Quiz, Progress, QuizAttempt
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
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        if not username or not password:
            return render_template('register.html', error='All fields required')
        
        if password != password_confirm:
            return render_template('register.html', error='Passwords do not match')
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists')
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

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
    
    # Calculate XP for next level
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
    
    # Mark lesson as completed
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
        user.add_xp(25)  # XP for completing lesson
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
        
        # Check if user already got XP for this quiz
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

# ==================== CODE EXECUTION ====================

def execute_code(code):
    """Safely execute Python code with restrictions"""
    import subprocess
    import signal
    
    # Dangerous imports to block
    dangerous_keywords = ['import os', 'import sys', 'import subprocess', '__import__', 'exec', 'eval', '__builtins__']
    
    for keyword in dangerous_keywords:
        if keyword in code.lower():
            return f"Error: '{keyword}' is not allowed for security reasons."
    
    try:
        # Run with timeout
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        output = result.stdout
        if result.stderr:
            output += '\nError:\n' + result.stderr
        
        return output if output else "Code executed successfully (no output)"
    
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out (>5 seconds). Check for infinite loops!"
    except Exception as e:
        return f"Error: {str(e)}"

# ==================== API ROUTES ====================

@app.route('/api/user')
@login_required
def api_user():
    user = User.query.get(session['user_id'])
    return jsonify(user.to_dict())

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('base.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('base.html'), 500

# ==================== DATABASE INITIALIZATION ====================

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)