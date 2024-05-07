from flask import Flask
from application.routes.user_routes import routes_blueprint
from application.middleware.logging_middleware import logging_middleware
from application.middleware.tracing_middleware import tracing_middleware
from application.models.user import db
from application.routes.kubernetes_routes import kubernetes_blueprint


from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app) 

# Apply Middleware
app = logging_middleware(app)
app = tracing_middleware(app)

# Configure SQLAlchemy after Flask app is created
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///khaos_engineer.db'  # Update with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications to avoid overhead

# Register the routes blueprint
app.register_blueprint(routes_blueprint)
app.register_blueprint(kubernetes_blueprint, url_prefix='/k8s')

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Define route for the home page
@app.route('/')
def home():
    return "Welcome to Khaos Engineering"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
