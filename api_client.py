import requests

from models import Book

class OpenLibraryClient:
    """
    A client for searching and retrieving book data from the Open Library API.
    """
    
    BASE_URL = 'https://openlibrary.org/search.json'
    
    def __init__(self):
        """
        Initializes the OpenLibraryClient with the base URL for the Open Library API.
        """
        self.base_url = self.BASE_URL
        
    def search_books(self, params):
        """
        Searches for books using the Open Library API with the given parameters.
        """
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)  # Set a timeout for the request
            response.raise_for_status()  # Raise an error for bad responses/if API request fails
            data = response.json()
            
            # Check if the API returned books
            if data.get('numFound', 0) == 0:
                print("No books found for the given search parameters.")
                return None
            
            books = data.get('docs', [])
            
            if not books:
                return None
            
            # Return the first book found
            return self.convert_to_book(books[0])
        
        except requests.exceptions.RequestException as error:
            print(f'API request failed: {error}')
            
          
        except ValueError as error:
            print(f'Could not read API response: {error}')
            return None
        
    def convert_to_book(self,data):
        """
        Convert Open Library's book data into our team's book format
        """
        
        # Get the title
        title = data.get('title', 'Unkown Title')
        
        # Get authors
        authors = data.get('author_name',[])
        
        # Get publication year
        first_publication_year = data.get('first_publish_year')
        
        # Get subjects
        subjects = data.get('subject',[])
        
        # Get page count
        pagecount = data.get('number_of_pages_median')
        
        # Get cover image
        cover_id = data.get('cover_i')
        if cover_id:
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            
        else:
            cover_url = None
            
        # Get ISBN
        isbn_list = data.get('isbn',[])
        if isbn_list:
            isbn = isbn_list[0] # Use the first isbn available
            
        else:
            isbn = None
            
            
        # Create and return our Book object
        return Book(title=title, authors=authors, first_publication_year=first_publication_year,
                    subjects=subjects, pagecount=pagecount, cover_url=cover_url, isbn=isbn)
        
        
    def search_by_title(self,title):
        """
        Search for a book by title.
        """
        
        if not title:
            return None

        params = {"title": title,"limit": 1}  # Create search parameters for title

        return self.search_books(params)
    
    def search_by_author(self,author):
        """
        Search for a book by author.
        """
        if not author:
            return None

        params = {"author": author,"limit": 1} # Create search parameters for author
        
        return self.search_books(params)
    
    def search_by_isbn(self,isbn):
        """
        Search for a book by ISBN.
        """
        if not isbn:
            return None

        params = {"isbn": isbn,"limit": 1} # Create search parameters for isbn

        return self.search_books(params)
