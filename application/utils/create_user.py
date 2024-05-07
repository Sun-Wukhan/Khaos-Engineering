import os
import requests
from requests.adapters import HTTPAdapter, Retry

def get_api_url():
    # Default to 127.0.0.1:5000 if no environment variable is set
    return os.getenv('API_BASE_URL', 'http://127.0.0.1:5000')

def create_user():
    url = f'{get_api_url()}/create_user'

    # Get user input with validation
    name = input("Enter username: ").strip()
    while not name:
        name = input("Username cannot be empty. Please enter a valid username: ").strip()

    password = input("Enter password: ").strip()
    while not password:
        password = input("Password cannot be empty. Please enter a valid password: ").strip()

    role = input("Enter role (admin/user): ").strip().lower()
    while role not in ['admin', 'user']:
        role = input("Invalid role. Please enter 'admin' or 'user': ").strip().lower()

    # Create data payload
    data = {
        'name': name,
        'password': password,
        'role': role
    }

    # Retry strategy
    retry_strategy = Retry(
        total=3,  # Number of retries
        backoff_factor=1,  # Wait 1s, 2s, 4s between retries
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
        method_whitelist=["POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("http://", adapter)
    http.mount("https://", adapter)

    # Send POST request to create user
    try:
        response = http.post(url, json=data)
        response.raise_for_status()  # Raise exception for HTTP errors (4xx or 5xx)
        print("User created successfully!")
        print(response.json())  # Print the response from the server
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err} (Status code: {response.status_code})")
        if response.status_code == 400:
            print("Invalid request data. Please ensure the user details are correct.")
        elif response.status_code == 401:
            print("Unauthorized. Please check your credentials.")
        elif response.status_code == 403:
            print("Forbidden. You do not have permission to perform this action.")
        elif response.status_code == 404:
            print("The endpoint was not found. Please verify the API URL.")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    create_user()
