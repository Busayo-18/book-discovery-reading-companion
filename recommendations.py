def get_similar_books(book, all_books=None):
    """Find books that are similar to the selected book."""

    if not book:
        return []

    if not all_books:
        return []

    results = []

    book_author = book.get("author", "").lower()
    book_subjects = book.get("subjects", [])

    for other_book in all_books:
        if other_book == book:
            continue

        other_author = other_book.get("author", "").lower()
        other_subjects = other_book.get("subjects", [])

        score = 0

        if book_author and book_author == other_author:
            score += 2

        for subject in book_subjects:
            if subject in other_subjects:
                score += 1

        if score > 0:
            results.append((score, other_book))

    results.sort(reverse=True, key=lambda item: item[0])

    return [book for score, book in results[:5]]
