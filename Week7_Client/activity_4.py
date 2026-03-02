import requests
from typing import Dict, Any, Optional

BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 5  # seconds


def print_book(book: Dict[str, Any]) -> None:
    """Nicely prints book details."""
    print("Book {")
    for key, val in book.items():
        print(f"\t{key}: {val}")
    print("}")


def get_book(book_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a book by ID from the API."""
    try:
        response = requests.get(f"{BASE_URL}/books/{book_id}", timeout=TIMEOUT)
        print(f"GET status code: {response.status_code}")

        response.raise_for_status()  # Raise exception for 4xx/5xx

        book = response.json()
        print_book(book)
        return book

    except requests.exceptions.RequestException as e:
        print(f"Error fetching book {book_id}: {e}")
    except ValueError:
        print("Failed to decode JSON response.")
    return None


def remove_book(book_id: int) -> bool:
    """Delete a book by ID."""
    try:
        response = requests.delete(f"{BASE_URL}/books/{book_id}", timeout=TIMEOUT)
        print(f"DELETE status code: {response.status_code}")

        response.raise_for_status()
        data = response.json()
        print(f"Delete result: {data.get('message')}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error deleting book {book_id}: {e}")
    except ValueError:
        print("Failed to decode JSON response.")
    return False


if __name__ == "__main__":
    book_id = 206

    print("***** Book information before delete *****")
    get_book(book_id)

    print("***** Deleting Book *****")
    success = remove_book(book_id)

    if success:
        print("***** Book information after delete *****")
        get_book(book_id)