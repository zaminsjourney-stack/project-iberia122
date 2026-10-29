from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests from Netlify to your local machine

# Setup structured logging to capture authentication events
logging.basicConfig(
    filename='auth_events.log',
    level=logging.INFO,
    format='%(asctime)s | IP: %(ip)s | User: %(user)s | Status: %(status)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Valid credentials for testing
USERS = {
    "admin": "1234",
    "alice": "sec2026",
    "bob": "cyber456"
}

@app.route('/api/login', methods=['POST'])
def handle_login():
    # Capture the client IP address (from Ngrok headers or direct request)
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')

    # Authenticate user credentials
    if username in USERS and USERS[username] == password:
        logging.info("Login Successful", extra={'ip': client_ip, 'user': username, 'status': 'SUCCESS'})
        return jsonify({"success": True, "message": "Login successful!"})
    else:
        logging.warning("Login Failed", extra={'ip': client_ip, 'user': username, 'status': 'FAILED'})
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)