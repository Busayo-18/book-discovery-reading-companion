import requests


def search_books(query, search_type="title"):
    """Search for books using the Open Library API."""

    if not query:
        return []

    if search_type == "author":
        url = "https://openlibrary.org/search.json"
        params = {"author": query}
    elif search_type == "isbn":
        url = "https://openlibrary.org/search.json"
        params = {"isbn": query}
    else:
        url = "https://openlibrary.org/search.json"
        params = {"title": query}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        books = []

        for book in data.get("docs", [])[:10]:
            books.append({
                "title": book.get("title", "Unknown title"),
                "author": ", ".join(book.get("author_name", ["Unknown author"])),
                "isbn": book.get("isbn", ["Not available"])[0],
                "cover_id": book.get("cover_i")
            })

        return books

    except requests.RequestException:
        return []
