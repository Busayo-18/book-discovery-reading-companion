def generate_reading_guide(book):
    title = book.get("title", "this book")
    author = book.get("author", "Unknown author")

    guide = f"""
Reading Guide

Title: {title}
Author: {author}

1. Read a few chapters at a time.
2. Write down the main ideas.
3. Note any important characters or topics.
4. Write down questions you have while reading.
5. At the end, summarize what you learned.

Enjoy reading!
"""
    return guide
