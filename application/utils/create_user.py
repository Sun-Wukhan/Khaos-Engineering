import requests

def create_user():
    url = 'http://localhost:5000/create_user'

    # Get user input
    name = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (admin/user): ")

    # Create data payload
    data = {
        'name': name,
        'password': password,
        'role': role
    }

    # Send POST request to create user
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        print("User created successfully!")
        print(response.json())  # Print the response from the server
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    create_user()
