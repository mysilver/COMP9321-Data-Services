import requests
from requests.auth import HTTPBasicAuth


def print_book(book):
    print("Book {")
    for key in book.keys():
        attr = str(key)
        val = str(book[key])
        print("\t" + attr + ":" + val)
    print("}")


def get_book(id, username, password):
    r = requests.get("http://127.0.0.1:5000/books/" + str(id), auth=HTTPBasicAuth(username, password))
    book = r.json()
    print("Get status Code:" + str(r.status_code))
    if r.ok:
        print_book(book)
        return book
    else:
        print('Error:' + book['message'])

if __name__ == '__main__':

    print("***** Book information With Valid Credentials *****")
    book = get_book(206, 'admin', 'admin')

    print("***** Book information With Invalid Credentials *****")
    book = get_book(206, 'xxxxxxxxx', 'yyyyyyyy')

