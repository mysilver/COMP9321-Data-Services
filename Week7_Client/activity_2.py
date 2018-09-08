import requests

if __name__ == '__main__':
    book = {
        "Date_of_Publication": 2018,
        "Publisher": "UNSW",
        "Author": "Nobody",
        "Title": "Nothing",
        "Flickr_URL": "http://somewhere",
        "Identifier": 2,
        "Place_of_Publication": "Sydney"
    }

    r = requests.post("http://127.0.0.1:5000/books", json=book)

    print("Status Code:" + str(r.status_code))
    resp = r.json()

    print(resp['message'])
