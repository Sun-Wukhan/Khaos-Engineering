from flask import Blueprint, request, jsonify
from application.models.user import db, User

# Create a Blueprint for routes
routes_blueprint = Blueprint('routes', __name__)

# Route to create a new user
@routes_blueprint.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    role = data.get('role')

    # Check if all required fields are provided
    if not all([name, password, role]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if the role is valid
    valid_roles = ['admin', 'user']  # Example roles
    if role not in valid_roles:
        return jsonify({'error': 'Invalid role'}), 400

    # Create a new user object
    new_user = User(name=name, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@routes_blueprint.route('/get_all_users', methods=['GET'])
def get_all_users(): 
    users = User.query.all()
    
    users_list = [{
        'id': user.id,
        'name': user.name,
        'role': user.role
    } for user in users 
    ]
    return jsonify(users_list), 200
