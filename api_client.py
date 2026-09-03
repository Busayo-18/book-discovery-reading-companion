import requests
from models import Book


class OpenLibraryClient:
    """
    A client for searching and retrieving book data
    from the Open Library API.
    """

    BASE_URL = "https://openlibrary.org/search.json"

    def __init__(self):
        self.base_url = self.BASE_URL

    def search_books(self, params):
        """
        Searches for books using the Open Library API with the given parameters.
        """
        params = dict(params)
        params['fields'] = 'title,author_name,first_publish_year,subject,number_of_pages_median,cover_i,isbn'

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('numFound', 0) == 0:
                return []

            books = data.get('docs', [])

            if not books:
                return []

            # Convert every result into a Book object
            return [
                self.convert_to_book(book_data)
                for book_data in books
            ]

        except requests.exceptions.RequestException as error:
            print(f'API request failed: {error}')
            return []

        except ValueError as error:
            print(f'Could not read API response: {error}')
            return []

    def convert_to_book(self, data):
            """
            Convert Open Library data into our Book format.
            """

            title = data.get('title', 'Unknown Title')

            authors = data.get('author_name', [])

            first_publication_year = data.get(
                'first_publish_year'
            )

            subjects = data.get('subject', [])

            pagecount = data.get(
                'number_of_pages_median'
            )

            cover_id = data.get('cover_i')

            if cover_id:
                cover_url = (
                    f"https://covers.openlibrary.org/"
                    f"b/id/{cover_id}-L.jpg"
                )
            else:
                cover_url = None

            isbn_list = data.get('isbn', [])

            if isbn_list:
                isbn = isbn_list[0]
            else:
                isbn = None

            return Book(
                title=title,
                authors=authors,
                first_publication_year=first_publication_year,
                subjects=subjects,
                pagecount=pagecount,
                cover_url=cover_url,
                isbn=isbn
            )

    def search_by_title(self, title):
            """
            Search for multiple books by title.
            """

            if not title:
                return []

            params = {'title': title, 'limit': 10}

            return self.search_books(params)

    def search_by_author(self, author):
            """
            Search for multiple books by author.
            """

            if not author:
                return []

            params = {'author': author,'limit': 10}

            return self.search_books(params)

    def search_by_isbn(self, isbn):
            """
            Search for books using ISBN.
            """

            if not isbn:
                return []

            params = {'isbn': isbn, 'limit': 10}

            return self.search_books(params)
        
    def search_by_subject(self, subject, limit=10):
            """
            Search for books that share a given subject.
            """
            if not subject:
                return []

            params = {"q": f'subject:"{subject}"', "limit": limit}

            return self.search_books(params)
