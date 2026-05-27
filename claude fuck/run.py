"""
run.py
Entry point for the Flask application
"""
import os
from app import create_app
from app.database import db


if __name__ == '__main__':
    # Create app
    app = create_app('development')
    
    # Run
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )