from flask import Flask, render_template, request, jsonify, session
from parser import GrootParser
from interpreter import GrootInterpreter
import uuid

app = Flask(__name__)
app.secret_key = 'groot-secret-key-change-in-production'

# Store interpreter instances per session
interpreters = {}

def get_interpreter():
    """Get or create interpreter instance for current session"""
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
    
    if session_id not in interpreters:
        interpreters[session_id] = GrootInterpreter()
    
    return interpreters[session_id]

@app.route('/')
def index():
    """Main page with the interpreter interface"""
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    """Execute Groot code and return results"""
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        
        if not code:
            return jsonify({'error': 'No code provided'})
        
        # Get parser and interpreter
        parser = GrootParser()
        interpreter = get_interpreter()
        
        # Capture output
        output = []
        original_print = print
        
        def capture_print(*args, **kwargs):
            output.append(' '.join(str(arg) for arg in args))
        
        # Temporarily replace print function
        import builtins
        builtins.print = capture_print
        
        try:
            # Parse and execute code
            tokens = parser.tokenize(code)
            if tokens:
                ast = parser.parse(tokens)
                interpreter.interpret(ast)
            
            # Get variable state
            state = interpreter.get_variable_state()
            
            return jsonify({
                'success': True,
                'output': '\n'.join(output) if output else '',
                'variables': state
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f"Error: {str(e)}",
                'variables': interpreter.get_variable_state()
            })
        
        finally:
            # Restore original print function
            builtins.print = original_print
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Server error: {str(e)}"
        })

@app.route('/reset', methods=['POST'])
def reset_interpreter():
    """Reset the interpreter state"""
    try:
        interpreter = get_interpreter()
        interpreter.reset()
        return jsonify({
            'success': True,
            'variables': interpreter.get_variable_state()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Error resetting: {str(e)}"
        })

@app.route('/examples')
def get_examples():
    """Get example Groot programs"""
    examples = {
        'Hello World': '''# Your first Groot program!
# This increments GROOT 6 times and prints it
I am GROOT!
I am GROOT!
I am GROOT!
I am GROOT!
I am GROOT!
I am GROOT''',
        
        'Variables': '''# Working with both variables
# Increment GROOT 3 times
I am GROOT!
I am GROOT!
I am GROOT!

# Increment groot 2 times  
I am groot!
I am groot!

# Print both values
I am GROOT
I am groot''',
        
        'Assignment': '''# Variable assignment
I am GROOT!
I am GROOT!
I am GROOT!

# Assign GROOT value to groot
I am groot, I am GROOT

# Print groot (should be 3)
I am groot''',
        
        'Arithmetic': '''# Simple arithmetic
I am GROOT!
I am GROOT!
I am GROOT!
I am groot!

# Add GROOT to groot and store in groot
I am groot! I am GROOT

# Print result
I am groot''',
        
        'Functions': '''# Function definition
I am... Groot,
    I am GROOT!
    I am GROOT!
    I am GROOT.

# Call function and assign result to groot
I am groot, I am... Groot

# Print result
I am groot''',

        'Complete Example': '''# Complete Groot program with functions and control flow
I am GROOT!
I am GROOT!
I am GROOT!

# Define a function
I am... Groot,
    I am GROOT!
    I am groot!
    I am GROOT.

# Use the function
I am groot, I am... Groot

# Print results
I am GROOT
I am groot'''
    }
    
    return jsonify(examples)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
