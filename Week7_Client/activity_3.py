import requests
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 5  # seconds


def print_book(book: Dict[str, Any]) -> None:
    """Nicely prints book details."""
    print("Book {")
    for key, val in book.items():
        print(f"\t{key}: {val}")
    print("}")


def get_book(book_id: int) -> Dict[str, Any] | None:
    """Retrieve a book by ID from the API."""
    try:
        response = requests.get(f"{BASE_URL}/books/{book_id}", timeout=TIMEOUT)
        print(f"GET status code: {response.status_code}")

        response.raise_for_status()  # Raise HTTPError for 4xx/5xx

        book = response.json()
        print_book(book)
        return book

    except requests.exceptions.RequestException as e:
        print(f"Error fetching book {book_id}: {e}")
    except ValueError:
        print("Failed to decode JSON response.")
    return None


def update_book(book_id: int, updated_data: Dict[str, Any]) -> bool:
    """Update a book by ID using PUT request."""
    try:
        response = requests.put(f"{BASE_URL}/books/{book_id}", json=updated_data, timeout=TIMEOUT)
        print(f"PUT status code: {response.status_code}")

        response.raise_for_status()
        data = response.json()
        print(f"Update result: {data.get('message')}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error updating book {book_id}: {e}")
    except ValueError:
        print("Failed to decode JSON response.")
    return False


if __name__ == "__main__":
    book_id = 206

    print("***** Book information before update *****")
    book = get_book(book_id)
    if book:
        # Update fields
        print("***** Updating Book Information *****")
        book['Author'] = 'Nobody'
        book['Date_of_Publication'] = 1879

        success = update_book(book_id, book)
        if success:
            print("***** Book information after update *****")
            get_book(book_id)