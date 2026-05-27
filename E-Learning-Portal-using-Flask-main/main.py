from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Course, Enrolled
import random
import string
from flask_mail import Mail, Message
from flask import *
import stripe


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/learn'
app.secret_key = 'Secret Key'
db.init_app(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'p11diyay@gmail.com' 
app.config['MAIL_PASSWORD'] = 'add password given by passkey for your gmail account, dont use your account password'
app.config['MAIL_DEBUG'] = True
mail = Mail(app)
stripe.api_key = "add the Stripe API key here"

def get_courses():
    return Course.query.all()

def send_course_added_notification(student_email, teacher, course):
    subject = f'New Course Added by {teacher.first_name} {teacher.last_name}'
    message = f"Dear student,\n\nA new course titled '{course.title}' has been added by {teacher.first_name} {teacher.last_name}." \
              f" You are currently enrolled in one of the courses by this teacher.\n\nYou can view the new course details on the platform."

    msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[student_email])
    msg.body = message
    mail.send(msg)

@app.route("/")
def home():
    status = True
    courses = get_courses()
    if 'user_id' not in session:
        return render_template('index.html', courses=courses)
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('index.html', courses=courses,logged_in=status,user=user)

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_id = session['user_id']
    user = User.query.get(user_id)
    if user.account=="teacher":
        return redirect(url_for('teacher_dashboard'))
    return redirect(url_for('student_dashboard'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        is_teacher = 'is_teacher' in request.form
        is_teacher = 'teacher' if is_teacher else 'student'

        otp = ''.join(random.choice(string.digits) for _ in range(6))

        subject = 'Your OTP for Registration'
        message = f'Your OTP is: {otp}'
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = message
        mail.send(msg)

        session['otp'] = otp
        session['user_data'] = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,
                'account':is_teacher
            }

        return redirect(url_for('verify_otp'))

    return render_template('register.html')


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if 'otp' in session and 'user_data' in session:
        if request.method == 'POST':
            user_entered_otp = request.form['otp']
            stored_otp = session['otp']

            if user_entered_otp == stored_otp:
                new_user = User(
                    first_name=session['user_data']['first_name'],
                    last_name=session['user_data']['last_name'],
                    email=session['user_data']['email'],
                    password=session['user_data']['password'],
                    account=session['user_data']['account']
                )
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect OTP. Please try again.', 'error')

        return render_template('verify_otp.html') 

    return render_template('index.html')

@app.route('/success')
def success():
    status=True
    if 'user_id' not in session:
        status=False
    user_id=session['user_id']
    user=User.query.get(user_id)
    message = flash('success')
    return render_template('success.html', message=message,logged_in=status, user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:

            db.session.commit()
            session['user_id'] = user.id

            if user.account=="teacher":

                return redirect(url_for('teacher_dashboard'))
            else:

                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html')


@app.route('/student_dashboard',methods=['GET', 'POST'])
def student_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    enrolled_courses = Enrolled.query.filter_by(student_id=user_id).all()

    enrolled_course_details = []

    for enrolled_course in enrolled_courses:
        course = Course.query.get(enrolled_course.course_id)
        enrolled_course_details.append(course)

    all_courses = Course.query.all()
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        if search_query:

            filtered_courses = [course for course in all_courses if search_query.lower() in course.title.lower()]
            return render_template('student_dashboard.html',search_results=filtered_courses, courses=all_courses,
                                   ecourses=enrolled_course_details, user=user)

    return render_template('student_dashboard.html', courses=all_courses, ecourses=enrolled_course_details, user=user)


@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    courses = Course.query.filter_by(user_id=user_id).all()

    enrolled_students = {}
    for course in courses:
        enrolled_students[course.id] = Enrolled.query.filter_by(course_id=course.id).all()

    enrolled_student_details = {}
    for course_id, students in enrolled_students.items():
        student_details = []
        for enrollment in students:
            user = User.query.get(enrollment.student_id)
            student_details.append(user)
        enrolled_student_details[course_id] = student_details
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('teacher_dashboard.html', user=user, courses=courses, enrolled_students=enrolled_students, enrolled_student_details=enrolled_student_details)


@app.route('/logout')
def logout():
    session.pop('user_id', None)  
    return redirect(url_for('login'))

@app.route('/course/<int:course_id>')
def course_details(course_id):

    course = Course.query.get(course_id)
    if 'user_id' not in session:
        return redirect(url_for('login'))
    session["course_id"]=course_id

    user_id = session['user_id']
    user = User.query.get(user_id)
    user_enrolled = Enrolled.query.filter_by(student_id=user_id, course_id=course_id).first() is not None

    return render_template('course_detail.html', course=course, user=user, user_enrolled=user_enrolled)


@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'GET':
        course_id = session.get('course_id')  
        if course_id is None:

            return redirect(url_for('student_dashboard'))

        user_id = session['user_id']
        new_enroll=Enrolled(enrollment=True, student_id=user_id, course_id=course_id)
        db.session.add(new_enroll)
        db.session.commit()
        session.pop('course_id', None)

        return redirect(url_for('student_dashboard'))

    return redirect(url_for('student_dashboard'))

@app.route('/edit_course/<int:course_id>', methods=['POST'])
def edit_course(course_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    user = User.query.get(user_id)

    if request.method == 'POST':

        new_title = request.form.get('newTitle')
        new_category = request.form.get('newCategory')
        new_price = request.form.get('newPrice')
        new_summary = request.form.get('newSummary')
        new_requirements = request.form.get('newRequirements')
        new_review = request.form.get('newReview')
        new_duration = request.form.get('newDuration')
        new_lectures = request.form.get('newLectures')
        new_quizzes = request.form.get('newQuizzes')

        course = Course.query.get(course_id)
        course.title = new_title
        course.category = new_category
        course.price = new_price
        course.summary = new_summary
        course.requirements = new_requirements
        course.review = new_review
        course.duration = new_duration
        course.lectures = new_lectures
        course.quizzes = new_quizzes

        db.session.commit()

        return redirect(url_for('teacher_dashboard'))

@app.route('/add_course', methods=['POST'])
def add_course():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    teacher = User.query.get(user_id)

    title = request.form.get('title')
    category = request.form.get('category')
    price = int(request.form.get('price'))
    summary = request.form.get('summary')
    requirements = request.form.get('requirements')
    review = request.form.get('review')
    duration = request.form.get('duration')
    lectures = int(request.form.get('lectures'))
    quizzes = int(request.form.get('quizzes'))

    new_course = Course(
        title=title,
        category=category,
        price=price,
        summary=summary,
        requirements=requirements,
        review=review,
        duration=duration,
        lectures=lectures,
        quizzes=quizzes,
        user=teacher 
    )

    db.session.add(new_course)
    db.session.commit()

    courses_by_teacher = Course.query.filter_by(user_id=user_id).all()
    students_to_notify = set()

    for course in courses_by_teacher:
        enrolled_students = Enrolled.query.filter_by(course_id=course.id).all()

        for student in enrolled_students:
            student_user = User.query.get(student.student_id)
            students_to_notify.add(student_user.email)

    sent_notifications = set()

    for student_email in students_to_notify:
        if student_email not in sent_notifications:
            send_course_added_notification(student_email, teacher, new_course)
            sent_notifications.add(student_email)

    flash("Course added successfully!", 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    course = Course.query.get(course_id)

    if course is not None and course.user_id == session['user_id']:

        db.session.delete(course)
        db.session.commit()
        flash('Course deleted successfully', 'success')
    else:
        flash('Failed to delete course', 'error')

    return redirect(url_for('teacher_dashboard'))

if __name__=="__main__":
    app.run(debug=True)
