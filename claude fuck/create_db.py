"""
create_db.py
Create database tables
"""
from app import create_app
from app.database import db

if __name__ == '__main__':
    app = create_app('development')
    
    with app.app_context():
        print('Creating database tables...')
        db.create_all()
        print('✓ Database tables created successfully')
        
        # Check if tables exist
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print('\nTables created:')
        for table in sorted(tables):
            print(f'  ✓ {table}')