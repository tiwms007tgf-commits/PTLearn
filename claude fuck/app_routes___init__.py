"""
app/routes/__init__.py
Register all route blueprints
"""
from flask import Blueprint

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
lessons_bp = Blueprint('lessons', __name__, url_prefix='/lessons')
quizzes_bp = Blueprint('quizzes', __name__, url_prefix='/quizzes')
code_lab_bp = Blueprint('code_lab', __name__, url_prefix='/code-lab')
progress_bp = Blueprint('progress', __name__, url_prefix='/progress')

# Import route functions
from .auth import *
from .lessons import *
from .quizzes import *
from .code_lab import *
from .progress import *