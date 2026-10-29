app = Flask(__name__)
CORS(app)

# 1. Initialize Flask-Limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
)

# 2. Configure Logging to 'auth_events.log'
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auth_events.log")

auth_logger = logging.getLogger("auth_events")
auth_logger.setLevel(logging.INFO)
auth_logger.propagate = False

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | IP: %(ip)s | User: %(username)s | Status: %(status)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_handler.setFormatter(file_formatter)
auth_logger.addHandler(file_handler)

# Console Output Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(file_formatter)
auth_logger.addHandler(console_handler)

# Dummy database for demonstration
USERS = {"admin": "12345", "alice": "sec2026", "bob": "password"}


def get_client_ip():
    """Extract real client IP if running behind proxy/ngrok."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr


# Custom error handler when rate limit is exceeded
@app.errorhandler(429)
def ratelimit_handler(e):
    client_ip = get_client_ip()
    auth_logger.warning(
        "Rate limit exceeded - Possible Brute Force",
        extra={"ip": client_ip, "username": "UNKNOWN", "status": "BLOCKED_429"},
    )
    return (
        jsonify(
            {
                "success": False,
                "error": "Too Many Requests",
                "message": "Rate limit exceeded. Try again in 1 minute.",
            }
        ),
        429,
    )


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Auth Server Running"})


# 3. Protected Login Route
@app.route("/api/login", methods=["POST"])
@limiter.limit("5 per minute")  # Blocks IP after 5 attempts in 60s
def handle_login():
    client_ip = get_client_ip()
    data = request.get_json(silent=True) or {}

    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    # Check credentials
    if username in USERS and USERS[username] == password:
        auth_logger.info(
            "Login Successful",
            extra={"ip": client_ip, "username": username, "status": "SUCCESS"},
        )
        return jsonify({"success": True, "message": "Login successful!"}), 200

    # Failed login
    auth_logger.warning(
        "Login Failed",
        extra={"ip": client_ip, "username": username, "status": "FAILED"},
    )
    return (
        jsonify({"success": False, "message": "Invalid username or password"}),
        401,
    )


if __name__ == "__main__":
    print(f"[*] Writing auth logs to: {LOG_FILE}")
    app.run(host="0.0.0.0", port=5000, debug=False)
