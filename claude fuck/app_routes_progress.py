"""
app/routes/progress.py
Progress tracking and dashboard routes
"""
from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from . import progress_bp
from ..services.gamification_service import GamificationService
from ..services.lesson_service import LessonService
from ..services.quiz_service import QuizService


@progress_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    # Get all progress data
    xp_history = GamificationService.get_xp_history(current_user.id, limit=10)
    achievements = GamificationService.get_user_achievements(current_user.id)
    quiz_results = QuizService.get_user_quiz_results(current_user.id, limit=5)
    learning_stats = LessonService.get_learning_stats(current_user.id)
    quiz_stats = QuizService.get_quiz_stats(current_user.id)
    
    return render_template('dashboard.html',
                          user=current_user,
                          xp_history=xp_history,
                          achievements=achievements,
                          quiz_results=quiz_results,
                          learning_stats=learning_stats,
                          quiz_stats=quiz_stats)


@progress_bp.route('/analytics')
@login_required
def analytics():
    """Detailed analytics page"""
    learning_stats = LessonService.get_learning_stats(current_user.id)
    quiz_stats = QuizService.get_quiz_stats(current_user.id)
    xp_history = GamificationService.get_xp_history(current_user.id, limit=30)
    achievements = GamificationService.get_user_achievements(current_user.id)
    
    return render_template('progress.html',
                          learning_stats=learning_stats,
                          quiz_stats=quiz_stats,
                          xp_history=xp_history,
                          achievements=achievements)


@progress_bp.route('/achievements')
@login_required
def achievements():
    """Achievements page"""
    achievements = GamificationService.get_user_achievements(current_user.id)
    
    return render_template('achievements.html',
                          achievements=achievements)


@progress_bp.route('/leaderboard')
@login_required
def leaderboard():
    """Global leaderboard"""
    leaderboard = GamificationService.get_leaderboard(limit=50)
    
    # Find current user's rank
    user_rank = None
    for entry in leaderboard:
        if entry['user_id'] == current_user.id:
            user_rank = entry['rank']
            break
    
    return render_template('leaderboard.html',
                          leaderboard=leaderboard,
                          user_rank=user_rank)


# API Endpoints

@progress_bp.route('/api/dashboard', methods=['GET'])
@login_required
def api_dashboard():
    """API: Get dashboard data"""
    return jsonify({
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'display_name': current_user.display_name,
            'level': current_user.level,
            'total_xp': current_user.total_xp,
            'xp_progress': current_user.get_xp_progress(),
            'current_streak': current_user.current_streak,
            'longest_streak': current_user.longest_streak,
            'avatar_color': current_user.avatar_color
        },
        'xp_history': GamificationService.get_xp_history(current_user.id, limit=10),
        'achievements': GamificationService.get_user_achievements(current_user.id),
        'learning_stats': LessonService.get_learning_stats(current_user.id),
        'quiz_stats': QuizService.get_quiz_stats(current_user.id)
    })


@progress_bp.route('/api/xp-history', methods=['GET'])
@login_required
def api_xp_history():
    """API: Get XP history"""
    limit = request.args.get('limit', 20, type=int)
    history = GamificationService.get_xp_history(current_user.id, limit=limit)
    return jsonify(history)


@progress_bp.route('/api/leaderboard', methods=['GET'])
@login_required
def api_leaderboard():
    """API: Get leaderboard"""
    limit = request.args.get('limit', 50, type=int)
    leaderboard = GamificationService.get_leaderboard(limit=limit)
    return jsonify(leaderboard)


@progress_bp.route('/api/achievements', methods=['GET'])
@login_required
def api_achievements():
    """API: Get achievements"""
    achievements = GamificationService.get_user_achievements(current_user.id)
    return jsonify(achievements)


@progress_bp.route('/api/stats', methods=['GET'])
@login_required
def api_stats():
    """API: Get comprehensive stats"""
    return jsonify({
        'learning': LessonService.get_learning_stats(current_user.id),
        'quizzes': QuizService.get_quiz_stats(current_user.id)
    })