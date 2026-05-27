"""
app/services/lesson_service.py
Lesson management and progress tracking
"""
from ..models import Lesson, LessonProgress, User
from ..database import db
from datetime import datetime


class LessonService:
    """Handle lesson operations"""
    
    @staticmethod
    def get_all_lessons(topic=None):
        """Get all lessons, optionally filtered by topic"""
        query = Lesson.query.order_by(Lesson.order, Lesson.created_at)
        
        if topic:
            query = query.filter_by(topic=topic)
        
        lessons = query.all()
        
        return [LessonService._lesson_to_dict(lesson) for lesson in lessons]
    
    @staticmethod
    def get_lesson_by_slug(slug):
        """Get single lesson by slug"""
        lesson = Lesson.get_by_slug(slug)
        if not lesson:
            return None
        
        return LessonService._lesson_to_dict(lesson)
    
    @staticmethod
    def get_lesson_with_progress(slug, user_id):
        """Get lesson with user's progress data"""
        lesson = Lesson.get_by_slug(slug)
        if not lesson:
            return None
        
        lesson_dict = LessonService._lesson_to_dict(lesson)
        
        # Get user progress
        progress = LessonProgress.query.filter_by(
            user_id=user_id,
            lesson_id=lesson.id
        ).first()
        
        lesson_dict['user_progress'] = {
            'completed': progress.completed if progress else False,
            'completed_at': progress.completed_at.isoformat() if progress and progress.completed_at else None,
            'code_attempted': progress.code_attempted if progress else None
        }
        
        # Get associated quizzes
        from .quiz_service import QuizService
        lesson_dict['quizzes'] = [
            {
                'id': quiz.id,
                'title': quiz.title,
                'description': quiz.description,
                'passing_score': quiz.passing_score
            }
            for quiz in lesson.quizzes
        ]
        
        return lesson_dict
    
    @staticmethod
    def mark_lesson_complete(user_id, lesson_id, code_attempted=None):
        """Mark lesson as completed"""
        user = User.get_by_id(user_id)
        lesson = Lesson.query.get(lesson_id)
        
        if not user or not lesson:
            return {'error': 'Invalid user or lesson'}
        
        # Get or create progress record
        progress = LessonProgress.query.filter_by(
            user_id=user_id,
            lesson_id=lesson_id
        ).first()
        
        if not progress:
            progress = LessonProgress(
                user_id=user_id,
                lesson_id=lesson_id
            )
            db.session.add(progress)
        
        progress.completed = True
        progress.completed_at = datetime.utcnow()
        progress.code_attempted = code_attempted
        
        db.session.commit()
        
        # Award XP if first completion
        from .gamification_service import GamificationService
        xp_result = GamificationService.award_lesson_xp(user_id, lesson_id)
        
        return {
            'lesson_id': lesson_id,
            'completed': True,
            'xp_awarded': xp_result.get('xp_awarded', 0),
            'new_level': xp_result.get('new_level'),
            'level_up': xp_result.get('level_up')
        }
    
    @staticmethod
    def get_user_lesson_progress(user_id):
        """Get user's progress on all lessons"""
        progress_records = LessonProgress.query.filter_by(
            user_id=user_id
        ).all()
        
        progress_dict = {}
        for record in progress_records:
            progress_dict[record.lesson_id] = {
                'completed': record.completed,
                'completed_at': record.completed_at.isoformat() if record.completed_at else None
            }
        
        return progress_dict
    
    @staticmethod
    def get_learning_path():
        """Get structured learning path grouped by topic"""
        topics = {}
        lessons = Lesson.query.order_by(
            Lesson.topic,
            Lesson.order,
            Lesson.created_at
        ).all()
        
        for lesson in lessons:
            topic = lesson.topic or 'Other'
            if topic not in topics:
                topics[topic] = []
            
            topics[topic].append(LessonService._lesson_to_dict(lesson))
        
        return topics
    
    @staticmethod
    def get_learning_stats(user_id):
        """Get learning statistics for user"""
        progress_records = LessonProgress.query.filter_by(
            user_id=user_id,
            completed=True
        ).all()
        
        total_lessons = Lesson.query.count()
        completed_lessons = len(progress_records)
        
        # Get topics and count by topic
        topics_completed = {}
        for record in progress_records:
            topic = record.lesson.topic or 'Other'
            topics_completed[topic] = topics_completed.get(topic, 0) + 1
        
        return {
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'completion_percentage': int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0,
            'topics_in_progress': len(topics_completed),
            'topics': topics_completed
        }
    
    @staticmethod
    def _lesson_to_dict(lesson):
        """Convert lesson model to dictionary"""
        return {
            'id': lesson.id,
            'title': lesson.title,
            'slug': lesson.slug,
            'description': lesson.description,
            'content': lesson.content,
            'code_example': lesson.code_example,
            'difficulty': lesson.difficulty,
            'topic': lesson.topic,
            'order': lesson.order,
            'created_at': lesson.created_at.isoformat()
        }