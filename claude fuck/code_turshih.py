"""
app/services/code_executor.py
Safe Python code execution with sandboxing
"""
import subprocess
import sys
import os
from datetime import timedelta
import tempfile
import signal


class CodeExecutionError(Exception):
    """Code execution error"""
    pass


class CodeExecutor:
    """Execute Python code safely"""
    
    # Restricted built-ins
    RESTRICTED_BUILTINS = {
        'eval', 'exec', 'compile', '__import__', 'open', 'input',
        'globals', 'locals', 'vars', 'dir', 'help', 'getattr', 'setattr',
        'delattr', 'type', 'super', 'classmethod', 'staticmethod'
    }
    
    ALLOWED_MODULES = ['math', 'random', 'string', 'collections', 'itertools']
    
    @staticmethod
    def execute(code, timeout=5):
        """
        Execute Python code safely with timeout
        Returns: {'success': bool, 'output': str, 'error': str}
        """
        try:
            # Validate code
            CodeExecutor._validate_code(code)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False,
                dir='/tmp'
            ) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute with timeout
                result = subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                return {
                    'success': result.returncode == 0,
                    'output': result.stdout,
                    'error': result.stderr,
                    'exit_code': result.returncode
                }
            
            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'output': '',
                    'error': f'Code execution timeout (limit: {timeout}s)'
                }
            
            finally:
                # Clean up
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
        
        except CodeExecutionError as e:
            return {
                'success': False,
                'output': '',
                'error': str(e)
            }
        
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Execution error: {str(e)}'
            }
    
    @staticmethod
    def _validate_code(code):
        """Validate code for safety"""
        if not isinstance(code, str):
            raise CodeExecutionError('Code must be a string')
        
        if len(code) > 10000:
            raise CodeExecutionError('Code exceeds maximum length (10000 chars)')
        
        # Check for restricted builtins
        for builtin in CodeExecutor.RESTRICTED_BUILTINS:
            if builtin in code:
                raise CodeExecutionError(f'Use of "{builtin}" is not allowed')
        
        # Check for file operations
        if 'os.' in code or 'sys.' in code or 'subprocess' in code:
            raise CodeExecutionError('File and system operations are not allowed')
        
        # Check for restricted imports (simple check)
        lines = code.split('\n')
        for line in lines:
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                # Extract module name
                parts = line.split()
                if len(parts) >= 2:
                    module = parts[1].split('.')[0]
                    if module not in CodeExecutor.ALLOWED_MODULES:
                        raise CodeExecutionError(
                            f'Module "{module}" is not allowed. '
                            f'Allowed: {", ".join(CodeExecutor.ALLOWED_MODULES)}'
                        )
        
        # Try to compile to catch syntax errors early
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            raise CodeExecutionError(f'Syntax error: {str(e)}')
    
    @staticmethod
    def get_allowed_modules():
        """Get list of allowed modules for frontend display"""
        return CodeExecutor.ALLOWED_MODULES
    
    @staticmethod
    def execute_for_lesson(code, test_cases=None, timeout=5):
        """
        Execute code with optional test cases
        Returns: {'success': bool, 'output': str, 'tests_passed': int, 'tests_total': int}
        """
        result = CodeExecutor.execute(code, timeout)
        
        if not result['success']:
            return result
        
        # Run test cases if provided
        if test_cases:
            tests_passed = 0
            tests_total = len(test_cases)
            
            for test in test_cases:
                test_code = f"{code}\n\n{test['code']}"
                test_result = CodeExecutor.execute(test_code, timeout)
                
                if test_result['success'] and test.get('expected') in test_result['output']:
                    tests_passed += 1
            
            result['tests_passed'] = tests_passed
            result['tests_total'] = tests_total
            result['tests_passed_percentage'] = int((tests_passed / tests_total) * 100)
        
        return result


class AnalyticsService:
    """User analytics and progress tracking"""
    
    @staticmethod
    def get_user_progress(user_id):
        """Get comprehensive user progress"""
        from ..models import LessonProgress, QuizResult, Achievement
        
        # Lessons
        lessons_completed = LessonProgress.query.filter_by(
            user_id=user_id,
            completed=True
        ).count()
        
        total_lessons = LessonProgress.query.filter_by(
            user_id=user_id
        ).count()
        
        # Quizzes
        quizzes_passed = QuizResult.query.filter_by(
            user_id=user_id,
            passed=True
        ).count()
        
        quizzes_attempted = QuizResult.query.filter_by(
            user_id=user_id
        ).count()
        
        # Achievements
        from ..models import UserAchievement
        achievements_unlocked = UserAchievement.query.filter_by(
            user_id=user_id
        ).count()
        
        return {
            'lessons': {
                'completed': lessons_completed,
                'total': total_lessons,
                'percentage': int((lessons_completed / total_lessons * 100)) if total_lessons > 0 else 0
            },
            'quizzes': {
                'passed': quizzes_passed,
                'attempted': quizzes_attempted,
                'success_rate': int((quizzes_passed / quizzes_attempted * 100)) if quizzes_attempted > 0 else 0
            },
            'achievements': {
                'unlocked': achievements_unlocked
            }
        }