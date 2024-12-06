# database.py
import json

def save_data(data, filename="database.json"):
    """
    Saves data (in JSON format) to a file.
    """
    with open(filename, "w") as file:
        json.dump(data, file)
    print(f"Data saved to {filename}")

def load_data(filename="database.json"):
    """
    Loads data from a JSON file.
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"{filename} not found.")
        return None

# Example usage:
if __name__ == "__main__":
    sample_data = {"user": "John", "posts": ["Post 1", "Post 2"]}
    save_data(sample_data)
    data = load_data()
    print(data)
