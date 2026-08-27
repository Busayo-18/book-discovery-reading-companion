class Book:
    def __init__(self, title, authors, first_publication_year, subjects, pagecount, cover_url, isbn):
        self.title = title
        self.authors = authors
        self.first_publication_year = first_publication_year
        self.subjects = subjects
        self.pagecount = pagecount
        self.cover_url = cover_url
        self.isbn = isbn
        # Additional attributes for user interaction
        self.status = 'Want to Read'  # Default status 
        self.summary = None  # Default summary
        self.reading_level = None  # Default reading level
        self.discussion_questions = []  # Default discussion questions
        
        
    def to_dict(self):
        return {
            'title': self.title,
            'authors': self.authors,
            'first_publication_year': self.first_publication_year,
            'subjects': self.subjects,
            'pagecount': self.pagecount,
            'cover_url': self.cover_url,
            'isbn': self.isbn,
            'status': self.status,
            'summary': self.summary,
            'reading_level': self.reading_level,
            'discussion_questions': self.discussion_questions
        }
    
    @classmethod # classmethod decorator allows the method to be called on the class itself, rather than on instances of the class.    
    def from_dict(cls, data):
        book = cls( data['title'], data['authors'], data['first_publication_year'], data['subjects'], data['pagecount'], data['cover_url'], data['isbn'])
        book.status = data.get('status', 'want to read')
        book.summary = data.get('summary')
        book.reading_level = data.get('reading_level')
        book.discussion_questions = data.get('discussion_questions', [])
        return book