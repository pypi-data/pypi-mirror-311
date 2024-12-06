import inspect
import requests  # Import the requests library for HTTP requests

# Define a fun function to display code
def fun():
    print("This is the fun() function!")

# Define the get_request function to make GET requests
def get_request(url):
    """Makes a GET request."""
    response = requests.get(url)
    return response

# Define the post_request function to make POST requests
def post_request(url, data):
    """Makes a POST request."""
    response = requests.post(url, data=data)
    return response

# Automatically show code when the module is imported
print("Welcome to My Personal Request Module!")
print("Here's the code for some functions in this module:")

# Show the source code of the 'fun' function
function_code = inspect.getsource(fun)
print("\nCode for fun():")
print(function_code)

# Show the source code for the 'get_request' function
get_request_code = inspect.getsource(get_request)
print("\nCode for get_request():")
print(get_request_code)

# Show the source code for the 'post_request' function
post_request_code = inspect.getsource(post_request)
print("\nCode for post_request():")
print(post_request_code)

# Inform the user of the available functions
print("\nYou can now use the following functions:")
print("1. get_request(url) - Makes a GET request.")
print("2. post_request(url, data) - Makes a POST request.")
