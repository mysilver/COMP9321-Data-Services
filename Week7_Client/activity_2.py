import requests

BASE_URL = "http://127.0.0.1:5000"

def add_book(book: dict):
    """
    Adds a book to the API using POST /books.

    Args:
        book (dict): Dictionary representing the book with all required fields.

    Returns:
        dict: API response containing message and possibly other info.
    """
    try:
        response = requests.post(f"{BASE_URL}/books", json=book)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
        data = response.json()
        print(f"Success: {data.get('message')}")
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        try:
            print(response.json())
        except:
            print(response.text)
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")
    except ValueError:
        print("Failed to parse response JSON")
    return None

if __name__ == "__main__":
    # Example book to add
    new_book = {
        "Date_of_Publication": 2018,
        "Publisher": "UNSW",
        "Author": "Nobody",
        "Title": "Nothing",
        "Flickr_URL": "http://somewhere",
        "Identifier": 2,
        "Place_of_Publication": "Sydney"
    }

    add_book(new_book)