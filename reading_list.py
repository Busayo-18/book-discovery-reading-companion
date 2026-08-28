import json
from models import Book


class ReadingListManager:
    """
    Manages the user's reading list.
    It can:
    - Add books
    - Remove books
    - Update book status
    - View the reading list
    - Save the reading list to a JSON file
    - Load the reading list from a JSON file
    """

    VALID_STATUSES = ['Want to Read', 'Reading', 'Finished']

    def __init__(self, filename='data/reading_list.json'):
        """
        Create a ReadingListManager.
        filename is the file where the reading list will be saved.
        """
        self.filename = filename
        self.books = []

        # Load saved books when the application starts
        self.load_list()

    def add_book(self, book):
        """Add a Book object to the reading list."""

        if not isinstance(book, Book):
            print('Error: Only Book objects can be added.')
            return

        # Check if the book is already in the list
        for existing_book in self.books:
            if existing_book.isbn == book.isbn and book.isbn is not None:
                print('Book is already in your reading list.')
                return

        self.books.append(book)
        print(f'"{book.title}" has been added to your reading list.')

    def remove_book(self, isbn):
        """Remove a book from the reading list using its ISBN."""
        
        # Remove the book if the isbn does not match
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                print(f'"{book.title}" has been removed.')
                return

        print('Book was not found in your reading list.')

    def update_status(self, isbn, status):
        """Change the reading status of a book."""
        
        # Check that the requested status is valid
        if status not in self.VALID_STATUSES:
            print('Invalid status.')
            print('Choose: Want to Read, Reading, or Finished.')
            return
        
        # Find the book and update its status
        for book in self.books:
            if book.isbn == isbn:
                book.status = status
                print(f'"{book.title}" status updated to "{status}".')
                return

        print('Book was not found in your reading list.')

    def view_list(self):
        """Display all books in the reading list."""

        if not self.books:
            print('Your reading list is empty.')
            return

        print("\n===== MY READING LIST =====")

        for number, book in enumerate(self.books, start=1):
            print(f"\n{number}. {book.title}")
            print(f"   Author(s): {', '.join(book.authors)}")
            print(f"   Status: {book.status}")
            print(f"   ISBN: {book.isbn}")

    def save_list(self):
        """Save the reading list to a JSON file."""

        try:
            data = []

            for book in self.books:
                data.append(book.to_dict())

            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)

            print('Reading list saved successfully.')

        except OSError as error:
            print(f'Could not save reading list: {error}')

    def load_list(self):
        """Load the reading list from a JSON file."""

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Handle an empty JSON file
            if not data:
                self.books = []
                return

            # Make sure the JSON contains a list
            if not isinstance(data, list):
                print('Invalid reading list format.')
                self.books = []
                return

            self.books = []

            for book_data in data:
                try:
                    book = Book.from_dict(book_data)
                    self.books.append(book) # Add the book to the reading list

                except (KeyError, TypeError) as error:
                    print(f'Skipping invalid book data: {error}')

            print('Reading list loaded successfully.')

        except FileNotFoundError:
            # The file doesn't exist yet.
            # That's okay because this may be the first time
            # the application is being used.
            self.books = []

        except json.JSONDecodeError:
            # The file exists but contains invalid JSON.
            print("Reading list file contains invalid JSON.")
            self.books = []

        except OSError as error:
            print(f'Could not load reading list: {error}')
            self.books = []