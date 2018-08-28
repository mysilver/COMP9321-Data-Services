import requests


def print_book(book):
    print("Book {")
    for key in book.keys():
        attr = str(key)
        if isinstance(book[key], unicode):
            val = str(book[key].encode('utf-8'))
        else:
            val = str(book[key])

        print("\t" + attr + ":" + val)
    print("}")


def get_book(id):
    r = requests.get("http://127.0.0.1:5000/books/" + str(id))
    book = r.json()
    print("Get status Code:" + str(r.status_code))
    print_book(book)
    return book


if __name__ == '__main__':

    print("***** Book information before update *****")
    book = get_book(206)

    # update the book information
    print("***** Updating Book Information *****")
    book['Author'] = 'Nobody'
    r = requests.put("http://127.0.0.1:5000/books/206", json=book)
    print("Put status Code:" + str(r.status_code))
    print(r.json()['message'])

    print("***** Book information after update *****")
    book = get_book(206)

