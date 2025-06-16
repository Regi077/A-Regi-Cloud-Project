# The application is set to run in debug mode, which is useful for development.
# In production, it is recommended to set debug to False and use a WSGI server like Gunicorn or uWSGI.      
# The app listens on port 5000, which is the default port for Flask applications.
# The `endpoints` module is where the actual API endpoints are defined, handling requests and responses.

# Perfect—that means your backend API is set up and working exactly as it should!
# You just authenticated and successfully retrieved live data from your secured Flask API. Everything is running smoothly.

from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from endpoints import api

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["30/minute"]
)
limiter.init_app(app)

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
