import requests

# -------------------------
# API base URL
# -------------------------
BASE_URL = "http://127.0.0.1:5000"  # Update if your Flask app runs on a different host/port

# -------------------------
# Query parameters
# -------------------------
params = {
    "order": "Date_of_Publication",  # Sort by column (must match API column names)
    "ascending": True                # True = ascending, False = descending
}

# -------------------------
# Make GET request to /books
# -------------------------
response = requests.get(f"{BASE_URL}/books", params=params)

# -------------------------
# Handle response
# -------------------------
if response.status_code == 200:
    books = response.json()
    print(f"Retrieved {len(books)} books:")
    for book in books:
        print(f"{book['Identifier']} - {book['Title']} by {book['Author']} ({book['Date_of_Publication']})")
else:
    print(f"Failed to retrieve books: {response.status_code}")
    print(response.json())