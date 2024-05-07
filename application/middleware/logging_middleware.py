# middleware/logging_middleware.py
import logging
from flask import request

# Configure logging
logging.basicConfig(filename='config/logs/app.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def logging_middleware(app):
    @app.before_request
    def log_request():
        logger.info(f"Request: {request.method} {request.url}")

    @app.after_request
    def log_response(response):
        logger.info(f"Response: {response.status_code}")
        return response

    return app
