# req.py
import requests

def get(url, params=None, headers=None):
    """
    Sends a GET request to the provided URL with optional parameters and headers.
    """
    print(f"Sending GET request to {url}")
    response = requests.get(url, params=params, headers=headers)
    return response

def post(url, data=None, json=None, headers=None):
    """
    Sends a POST request to the provided URL with optional data, json, and headers.
    """
    print(f"Sending POST request to {url}")
    response = requests.post(url, data=data, json=json, headers=headers)
    return response

# Example usage:
if __name__ == "__main__":
    response = get("https://jsonplaceholder.typicode.com/posts")
    print(response.status_code)
    print(response.json())
