from flask import Flask, request, jsonify
import os
import subprocess
import ipaddress
from simpleeval import SimpleEval, FunctionNotDefined

app = Flask(__name__)

# Retrieve password from environment variable instead of hardcoding
PASSWORD = os.environ.get('PASSWORD', 'default_password')

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    if not name.isalnum():
        return jsonify({"error": "Invalid name"}), 400
    return f"Hello, {name}!"

# Secure ping route with input validation and no shell=True
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    try:
        ipaddress.ip_address(ip)  # Validate IP address
        result = subprocess.check_output(["ping", "-c", "1", ip])
        return result
    except ValueError:
        return jsonify({"error": "Invalid IP address"}), 400
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Ping failed", "details": str(e)}), 500

# Secure math expression evaluator
@app.route('/calculate')
    expression = request.args.get('expr')
    if not expression:
        return jsonify({"error": "No expression provided"}), 400
    # Handle '+' encoded as space
    expression = expression.replace(' ', '+')
    s = SimpleEval()
    try:
        result = s.eval(expression)
        return jsonify({"result": result})
    except (FunctionNotDefined, ValueError, SyntaxError, TypeError, ZeroDivisionError) as e:
        return jsonify({"error": "Invalid expression", "details": str(e)}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000) # Bind to localhost instead of all interfaces
