"""
app/services/gamification_service.py
Handles XP, levels, streaks, and achievements
"""
from ..models import User, XPHistory, UserAchievement, Achievement
from ..database import db
from datetime import datetime, timedelta


class GamificationService:
    """Handle all gamification mechanics"""
    
    @staticmethod
    def award_xp(user_id, amount, source, related_id=None):
        """Award XP to user and check for level up"""
        user = User.get_by_id(user_id)
        if not user:
            return False
        
        # Record XP
        xp_record = XPHistory(
            user_id=user_id,
            amount=amount,
            source=source,
            related_id=related_id
        )
        
        user.total_xp += amount
        db.session.add(xp_record)
        
        # Check for level up
        level_up = GamificationService.check_level_up(user)
        
        # Update streak
        user.update_streak()
        
        db.session.commit()
        
        return {
            'xp_awarded': amount,
            'new_total_xp': user.total_xp,
            'level_up': level_up,
            'new_level': user.level,
            'xp_progress': user.get_xp_progress()
        }
    
    @staticmethod
    def check_level_up(user):
        """Check if user leveled up and update accordingly"""
        level_up_occurred = False
        
        while True:
            xp_needed = user.calculate_xp_for_next_level()
            xp_at_current_level = sum(
                int(100 * (1.2 ** (i - 1))) for i in range(1, user.level)
            )
            xp_in_current_level = user.total_xp - xp_at_current_level
            
            if xp_in_current_level >= xp_needed:
                user.level += 1
                level_up_occurred = True
                
                # Check for level-based achievements
                GamificationService.check_achievement_unlock(
                    user.id,
                    f'level_{user.level}'
                )
            else:
                break
        
        return level_up_occurred
    
    @staticmethod
    def award_quiz_xp(user_id, quiz_id, score, is_perfect=False):
        """Award XP for quiz completion"""
        from .quiz_service import QuizService
        
        # Prevent duplicate rewards
        from ..models import QuizResult
        existing = QuizResult.query.filter_by(
            user_id=user_id,
            quiz_id=quiz_id
        ).first()
        
        if existing and existing.xp_earned > 0:
            return {'error': 'Already completed this quiz'}
        
        base_xp = 10  # From config
        bonus_xp = 5 if is_perfect else 0
        total_xp = base_xp + bonus_xp
        
        result = GamificationService.award_xp(
            user_id,
            total_xp,
            'quiz_perfect' if is_perfect else 'quiz_complete',
            related_id=quiz_id
        )
        
        # Check for quiz achievements
        GamificationService.check_achievement_unlock(
            user_id,
            'complete_quiz',
            metadata={'is_perfect': is_perfect}
        )
        
        return result
    
    @staticmethod
    def award_lesson_xp(user_id, lesson_id):
        """Award XP for lesson completion"""
        return GamificationService.award_xp(
            user_id,
            20,
            'lesson_complete',
            related_id=lesson_id
        )
    
    @staticmethod
    def get_streak_bonus(user_id):
        """Calculate streak bonus XP"""
        user = User.get_by_id(user_id)
        if not user:
            return 0
        
        # 1 XP per day of streak
        return user.current_streak
    
    @staticmethod
    def check_achievement_unlock(user_id, achievement_slug, metadata=None):
        """Check and unlock achievement if criteria met"""
        achievement = Achievement.query.filter_by(slug=achievement_slug).first()
        
        if not achievement:
            return False
        
        # Check if already unlocked
        existing = UserAchievement.query.filter_by(
            user_id=user_id,
            achievement_id=achievement.id
        ).first()
        
        if existing:
            return False
        
        # Unlock achievement
        user_achievement = UserAchievement(
            user_id=user_id,
            achievement_id=achievement.id
        )
        
        db.session.add(user_achievement)
        db.session.commit()
        
        return True
    
    @staticmethod
    def get_user_achievements(user_id):
        """Get all achievements for user"""
        user = User.get_by_id(user_id)
        if not user:
            return []
        
        achievements = []
        for achievement in user.achievements:
            user_ach = UserAchievement.query.filter_by(
                user_id=user_id,
                achievement_id=achievement.id
            ).first()
            
            achievements.append({
                'id': achievement.id,
                'slug': achievement.slug,
                'title': achievement.title,
                'description': achievement.description,
                'icon': achievement.icon,
                'unlocked_at': user_ach.unlocked_at.isoformat() if user_ach else None
            })
        
        return achievements
    
    @staticmethod
    def get_leaderboard(limit=10):
        """Get top users by XP"""
        users = User.query.order_by(
            User.level.desc(),
            User.total_xp.desc()
        ).limit(limit).all()
        
        leaderboard = []
        for idx, user in enumerate(users, 1):
            leaderboard.append({
                'rank': idx,
                'user_id': user.id,
                'username': user.username,
                'display_name': user.display_name,
                'level': user.level,
                'total_xp': user.total_xp,
                'avatar_color': user.avatar_color
            })
        
        return leaderboard
    
    @staticmethod
    def get_xp_history(user_id, limit=20):
        """Get recent XP activity"""
        records = XPHistory.query.filter_by(
            user_id=user_id
        ).order_by(XPHistory.created_at.desc()).limit(limit).all()
        
        history = []
        for record in records:
            history.append({
                'id': record.id,
                'amount': record.amount,
                'source': record.source,
                'badge': record.get_badge(),
                'timestamp': record.created_at.isoformat(),
                'time_ago': GamificationService._time_ago(record.created_at)
            })
        
        return history
    
    @staticmethod
    def _time_ago(dt):
        """Format datetime as 'time ago'"""
        now = datetime.utcnow()
        diff = now - dt
        
        seconds = diff.total_seconds()
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        
        if seconds < 60:
            return 'just now'
        elif minutes < 60:
            return f'{int(minutes)}m ago'
        elif hours < 24:
            return f'{int(hours)}h ago'
        elif days < 7:
            return f'{int(days)}d ago'
        else:
            return dt.strftime('%b %d')