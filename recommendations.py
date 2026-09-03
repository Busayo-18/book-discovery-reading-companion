def get_similar_books(book, api_client, reading_list_books=None, limit=5):
    """
    Find books similar to the given book.
    Checks the user's reading list first, then searches
    Open Library itself using the book's subjects.
    """

    if not book:
        return []

    results = []
    seen_isbns = {book.isbn}

    # Check the reading list first (free, no API call needed)
    if reading_list_books:
        for other_book in reading_list_books:
            if other_book.isbn in seen_isbns:
                continue

            score = 0

            if set(book.authors) & set(other_book.authors):
                score += 2

            score += len(set(book.subjects) & set(other_book.subjects))

            if score > 0:
                results.append((score, other_book))
                seen_isbns.add(other_book.isbn)

    # Then search Open Library using the book's top subject
    if book.subjects:
        found = api_client.search_by_subject(book.subjects[0], limit=limit + 5)

        for other_book in found:
            if other_book.isbn in seen_isbns:
                continue

            results.append((1, other_book))
            seen_isbns.add(other_book.isbn)

    results.sort(reverse=True, key=lambda item: item[0])

    return [b for score, b in results[:limit]]