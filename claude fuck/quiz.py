"""
app/services/quiz_service.py
Quiz handling and grading
"""
from ..models import Quiz, QuizResult, User
from ..database import db
from datetime import datetime
import json


class QuizService:
    """Handle quiz operations"""
    
    @staticmethod
    def get_quiz_with_questions(quiz_id):
        """Get quiz with questions"""
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return None
        
        return {
            'id': quiz.id,
            'lesson_id': quiz.lesson_id,
            'title': quiz.title,
            'description': quiz.description,
            'passing_score': quiz.passing_score,
            'questions': quiz.get_questions()
        }
    
    @staticmethod
    def submit_quiz_answers(user_id, quiz_id, answers, time_spent):
        """Submit quiz answers and grade"""
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {'error': 'Quiz not found'}
        
        questions = quiz.get_questions()
        score = QuizService.grade_quiz(answers, questions)
        passed = score >= quiz.passing_score
        
        # Store result
        result = QuizResult(
            user_id=user_id,
            quiz_id=quiz_id,
            score=score,
            passed=passed,
            time_spent=time_spent,
            xp_earned=0  # Will be set by gamification service
        )
        result.set_answers(answers)
        
        db.session.add(result)
        db.session.commit()
        
        return {
            'quiz_id': quiz_id,
            'score': score,
            'passed': passed,
            'passing_score': quiz.passing_score,
            'result_id': result.id,
            'feedback': QuizService.get_quiz_feedback(answers, questions)
        }
    
    @staticmethod
    def grade_quiz(answers, questions):
        """Grade quiz answers"""
        if not questions:
            return 0
        
        correct_count = 0
        
        for idx, question in enumerate(questions):
            question_id = str(idx)
            user_answer = answers.get(question_id)
            
            if question['type'] == 'multiple_choice':
                if user_answer == question.get('correct_answer'):
                    correct_count += 1
            elif question['type'] == 'text_input':
                # Case-insensitive comparison
                correct_answer = question.get('correct_answer', '').strip().lower()
                user_answer_clean = (user_answer or '').strip().lower()
                if user_answer_clean == correct_answer:
                    correct_count += 1
        
        percentage = int((correct_count / len(questions)) * 100) if questions else 0
        return percentage
    
    @staticmethod
    def get_quiz_feedback(answers, questions):
        """Generate detailed feedback for each question"""
        feedback = []
        
        for idx, question in enumerate(questions):
            question_id = str(idx)
            user_answer = answers.get(question_id)
            correct_answer = question.get('correct_answer')
            
            is_correct = False
            if question['type'] == 'multiple_choice':
                is_correct = user_answer == correct_answer
            elif question['type'] == 'text_input':
                is_correct = (user_answer or '').strip().lower() == \
                            (correct_answer or '').strip().lower()
            
            feedback.append({
                'question_id': idx,
                'question': question.get('question'),
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question.get('explanation'),
                'type': question['type']
            })
        
        return feedback
    
    @staticmethod
    def get_user_quiz_results(user_id, limit=10):
        """Get user's quiz results"""
        results = QuizResult.query.filter_by(
            user_id=user_id
        ).order_by(QuizResult.created_at.desc()).limit(limit).all()
        
        quiz_results = []
        for result in results:
            quiz_results.append({
                'id': result.id,
                'quiz_id': result.quiz_id,
                'quiz_title': result.quiz.title,
                'lesson_id': result.quiz.lesson_id,
                'score': result.score,
                'passed': result.passed,
                'xp_earned': result.xp_earned,
                'time_spent': result.time_spent,
                'timestamp': result.created_at.isoformat()
            })
        
        return quiz_results
    
    @staticmethod
    def get_quiz_stats(user_id):
        """Get quiz statistics for user"""
        results = QuizResult.query.filter_by(user_id=user_id).all()
        
        if not results:
            return {
                'total_quizzes': 0,
                'passed': 0,
                'passed_percentage': 0,
                'average_score': 0,
                'total_xp_earned': 0
            }
        
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        total_xp = sum(r.xp_earned for r in results)
        avg_score = sum(r.score for r in results) / total if total > 0 else 0
        
        return {
            'total_quizzes': total,
            'passed': passed,
            'passed_percentage': int((passed / total) * 100) if total > 0 else 0,
            'average_score': int(avg_score),
            'total_xp_earned': total_xp
        }