reading_list = []


def add_book(book):
    reading_list.append(book)
    return True


def update_status(book, status):
    book["status"] = status
    return True


def get_reading_list():
    return reading_list