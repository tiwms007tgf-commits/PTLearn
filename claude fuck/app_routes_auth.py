"""
app/routes/auth.py
Authentication routes: register, login, logout
"""
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user
from . import auth_bp
from ..models import User
from ..services.auth_service import AuthService
from ..database import db


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        user, errors = AuthService.register_user(username, email, password)
        
        if user:
            login_user(user)
            flash('Account created successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            for error in errors:
                flash(error, 'error')
    
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login user"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        user, error = AuthService.login_user(username, password)
        
        if user:
            login_user(user, remember=request.form.get('remember'))
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash(error, 'error')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """User profile"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        data = {
            'display_name': request.form.get('display_name'),
            'bio': request.form.get('bio'),
            'theme': request.form.get('theme'),
            'avatar_color': request.form.get('avatar_color'),
        }
        
        # Handle password change
        if request.form.get('new_password'):
            data['current_password'] = request.form.get('current_password')
            data['new_password'] = request.form.get('new_password')
        
        errors = AuthService.update_profile(current_user, data)
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('auth.profile'))
    
    stats = AuthService.get_user_stats(current_user.id)
    return render_template('profile.html', stats=stats)


@auth_bp.route('/api/user', methods=['GET'])
def get_user_data():
    """API: Get current user data"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    stats = AuthService.get_user_stats(current_user.id)
    return jsonify(stats)