"""
app/routes/code_lab.py
Code execution and learning routes
"""
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from . import code_lab_bp
from ..services.code_executor import CodeExecutor


@code_lab_bp.route('/')
@login_required
def index():
    """Code lab page"""
    return render_template('code_lab.html')


@code_lab_bp.route('/api/execute', methods=['POST'])
@login_required
def execute_code():
    """API: Execute Python code"""
    if not request.is_json:
        return jsonify({'error': 'Invalid request'}), 400
    
    data = request.get_json()
    code = data.get('code', '')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    # Execute code
    result = CodeExecutor.execute(code, timeout=5)
    
    return jsonify(result)


@code_lab_bp.route('/api/validate', methods=['POST'])
@login_required
def validate_code():
    """API: Validate code syntax"""
    if not request.is_json:
        return jsonify({'error': 'Invalid request'}), 400
    
    data = request.get_json()
    code = data.get('code', '')
    
    try:
        compile(code, '<string>', 'exec')
        return jsonify({'valid': True})
    except SyntaxError as e:
        return jsonify({
            'valid': False,
            'error': str(e),
            'line': e.lineno
        })


@code_lab_bp.route('/api/allowed-modules')
@login_required
def get_allowed_modules():
    """API: Get allowed Python modules"""
    modules = CodeExecutor.get_allowed_modules()
    return jsonify({'modules': modules})


@code_lab_bp.route('/api/execute-with-tests', methods=['POST'])
@login_required
def execute_with_tests():
    """API: Execute code with test cases"""
    if not request.is_json:
        return jsonify({'error': 'Invalid request'}), 400
    
    data = request.get_json()
    code = data.get('code', '')
    test_cases = data.get('test_cases', [])
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    result = CodeExecutor.execute_for_lesson(code, test_cases, timeout=5)
    
    return jsonify(result)