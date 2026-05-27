"""
app/routes/lessons.py
Lesson routes: viewing lessons, marking complete
"""
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from . import lessons_bp
from ..services.lesson_service import LessonService
from ..services.gamification_service import GamificationService


@lessons_bp.route('/')
@login_required
def index():
    """List all lessons"""
    lessons = LessonService.get_all_lessons()
    user_progress = LessonService.get_user_lesson_progress(current_user.id)
    learning_stats = LessonService.get_learning_stats(current_user.id)
    
    # Add progress info to lessons
    for lesson in lessons:
        lesson['user_progress'] = user_progress.get(lesson['id'], {})
    
    return render_template('lessons.html',
                          lessons=lessons,
                          learning_stats=learning_stats)


@lessons_bp.route('/<slug>')
@login_required
def detail(slug):
    """View single lesson"""
    lesson = LessonService.get_lesson_with_progress(slug, current_user.id)
    
    if not lesson:
        flash('Lesson not found', 'error')
        return redirect(url_for('lessons.index'))
    
    return render_template('lesson_detail.html', lesson=lesson)


@lessons_bp.route('/api/<slug>', methods=['GET'])
@login_required
def get_lesson_data(slug):
    """API: Get lesson data"""
    lesson = LessonService.get_lesson_with_progress(slug, current_user.id)
    
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    
    return jsonify(lesson)


@lessons_bp.route('/api/<int:lesson_id>/complete', methods=['POST'])
@login_required
def mark_complete(lesson_id):
    """API: Mark lesson as complete"""
    code_attempted = request.json.get('code_attempted') if request.is_json else None
    
    result = LessonService.mark_lesson_complete(
        current_user.id,
        lesson_id,
        code_attempted=code_attempted
    )
    
    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify(result)


@lessons_bp.route('/api/path')
@login_required
def get_learning_path():
    """API: Get structured learning path"""
    path = LessonService.get_learning_path()
    return jsonify(path)


@lessons_bp.route('/api/by-topic/<topic>')
@login_required
def get_by_topic(topic):
    """API: Get lessons by topic"""
    lessons = LessonService.get_all_lessons(topic=topic)
    return jsonify(lessons)