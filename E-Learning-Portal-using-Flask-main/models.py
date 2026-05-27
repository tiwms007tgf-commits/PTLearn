from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    date_created = db.Column(DateTime, default=func.now())
    account = db.Column(db.String(12), default='student', nullable=False)



class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.String(1000), nullable=False)
    requirements = db.Column(db.String(2000), nullable=False)
    review = db.Column(db.String(250))
    duration = db.Column(db.String(50))
    lectures = db.Column(db.Integer, nullable=False)
    quizzes = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship("User", backref=db.backref("user", uselist=False))


class Enrolled(db.Model):
    __tablename__ = "enrolled"
    id = db.Column(db.Integer, primary_key=True)
    enrollment = db.Column(db.Boolean, nullable=False)
    student_id = db.Column(db.Integer, ForeignKey('user.id'))

    course_id = db.Column(db.Integer, ForeignKey('course.id'))
    course = db.relationship("Course", backref=db.backref("course"))