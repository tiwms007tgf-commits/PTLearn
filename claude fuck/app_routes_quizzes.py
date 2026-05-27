"""
app/routes/quizzes.py
Quiz routes: taking quizzes, submitting answers
"""
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from . import quizzes_bp
from ..services.quiz_service import QuizService
from ..services.gamification_service import GamificationService


@quizzes_bp.route('/')
@login_required
def index():
    """List quizzes"""
    results = QuizService.get_user_quiz_results(current_user.id, limit=20)
    stats = QuizService.get_quiz_stats(current_user.id)
    
    return render_template('quizzes.html',
                          results=results,
                          stats=stats)


@quizzes_bp.route('/<int:quiz_id>')
@login_required
def take_quiz(quiz_id):
    """Take quiz"""
    quiz = QuizService.get_quiz_with_questions(quiz_id)
    
    if not quiz:
        flash('Quiz not found', 'error')
        return redirect(url_for('quizzes.index'))
    
    return render_template('quiz.html', quiz=quiz)


@quizzes_bp.route('/api/<int:quiz_id>', methods=['GET'])
@login_required
def get_quiz_data(quiz_id):
    """API: Get quiz data"""
    quiz = QuizService.get_quiz_with_questions(quiz_id)
    
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    return jsonify(quiz)


@quizzes_bp.route('/api/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    """API: Submit quiz answers"""
    if not request.is_json:
        return jsonify({'error': 'Invalid request'}), 400
    
    data = request.get_json()
    answers = data.get('answers', {})
    time_spent = data.get('time_spent', 0)
    
    # Submit answers
    result = QuizService.submit_quiz_answers(
        current_user.id,
        quiz_id,
        answers,
        time_spent
    )
    
    if 'error' in result:
        return jsonify(result), 400
    
    # Award XP
    is_perfect = all(
        f['is_correct'] for f in result['feedback']
    )
    
    xp_result = GamificationService.award_quiz_xp(
        current_user.id,
        quiz_id,
        result['score'],
        is_perfect=is_perfect
    )
    
    result['xp'] = xp_result
    
    return jsonify(result)


@quizzes_bp.route('/api/results/<int:result_id>', methods=['GET'])
@login_required
def get_result_detail(result_id):
    """API: Get quiz result details"""
    from ..models import QuizResult
    
    result = QuizResult.query.get(result_id)
    
    if not result or result.user_id != current_user.id:
        return jsonify({'error': 'Result not found'}), 404
    
    return jsonify({
        'id': result.id,
        'quiz_id': result.quiz_id,
        'score': result.score,
        'passed': result.passed,
        'xp_earned': result.xp_earned,
        'time_spent': result.time_spent,
        'answers': result.get_answers(),
        'timestamp': result.created_at.isoformat()
    })


@quizzes_bp.route('/api/user-results')
@login_required
def get_user_results():
    """API: Get user's quiz results"""
    limit = request.args.get('limit', 20, type=int)
    results = QuizService.get_user_quiz_results(current_user.id, limit=limit)
    return jsonify(results)


@quizzes_bp.route('/api/stats')
@login_required
def get_stats():
    """API: Get quiz statistics"""
    stats = QuizService.get_quiz_stats(current_user.id)
    return jsonify(stats)