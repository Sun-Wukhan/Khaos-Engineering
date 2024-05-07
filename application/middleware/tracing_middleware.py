# middleware/tracing_middleware.py
import time
from flask import request

def tracing_middleware(app):
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def log_request_time(response):
        elapsed_time = time.time() - request.start_time
        app.logger.info(f"Request took: {elapsed_time} seconds")
        return response

    return app
