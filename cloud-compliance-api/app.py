# This is the main entry point for the Flask application.
# It initializes the Flask app, sets up CORS, rate limiting, and registers the API blueprint.   
# The app runs on port 5000 in debug mode.
# The endpoints are defined in the `endpoints.py` file, which handles various API requests.



from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from endpoints import api

app = Flask(__name__)
CORS(app)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["30/minute"])
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
