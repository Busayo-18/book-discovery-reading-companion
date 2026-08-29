import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Import functions from the other modules
from book_search import search_books
from reading_list import add_book, update_status
from reading_guide import generate_reading_guide
from recommendations import get_similar_books


class BookApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Book Discovery & Reading Companion")
        self.root.geometry("950x750")

        self.current_book = None
        self.cover_image = None

        # ---------------- TITLE ----------------

        title = tk.Label(
            root,
            text="📚 Book Discovery & Reading Companion",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        # ---------------- SEARCH ----------------

        search_frame = tk.Frame(root)
        search_frame.pack(pady=10)

        tk.Label(
            search_frame,
            text="Search by:"
        ).grid(row=0, column=0, padx=5)

        self.search_type = ttk.Combobox(
            search_frame,
            values=["Title", "Author", "ISBN"],
            state="readonly",
            width=15
        )
        self.search_type.current(0)
        self.search_type.grid(row=0, column=1, padx=5)

        self.search_entry = tk.Entry(
            search_frame,
            width=40
        )
        self.search_entry.grid(row=0, column=2, padx=5)

        search_button = tk.Button(
            search_frame,
            text="🔎 Search",
            command=self.search_book
        )
        search_button.grid(row=0, column=3, padx=5)

        # ---------------- BOOK DETAILS ----------------

        details_frame = tk.LabelFrame(
            root,
            text="Book Details",
            padx=15,
            pady=15
        )

        details_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # Cover image

        self.cover_label = tk.Label(
            details_frame,
            text="Book Cover",
            width=25,
            height=15
        )
        self.cover_label.pack(
            side="left",
            padx=20
        )

        # Book information

        info_frame = tk.Frame(details_frame)
        info_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.book_title = tk.Label(
            info_frame,
            text="Title:",
            font=("Arial", 13, "bold"),
            anchor="w"
        )
        self.book_title.pack(
            anchor="w",
            pady=5
        )

        self.book_author = tk.Label(
            info_frame,
            text="Author:",
            anchor="w"
        )
        self.book_author.pack(
            anchor="w",
            pady=5
        )

        self.book_isbn = tk.Label(
            info_frame,
            text="ISBN:",
            anchor="w"
        )
        self.book_isbn.pack(
            anchor="w",
            pady=5
        )

        self.book_description = tk.Label(
            info_frame,
            text="Description:",
            wraplength=600,
            justify="left",
            anchor="nw"
        )
        self.book_description.pack(
            anchor="w",
            pady=5
        )

        # ---------------- READING STATUS ----------------

        status_frame = tk.Frame(root)
        status_frame.pack(pady=10)

        tk.Label(
            status_frame,
            text="Reading Status:"
        ).pack(
            side="left",
            padx=5
        )

        self.status = ttk.Combobox(
            status_frame,
            values=[
                "Want to Read",
                "Currently Reading",
                "Completed"
            ],
            state="readonly",
            width=20
        )

        self.status.current(0)

        self.status.pack(
            side="left",
            padx=5
        )

        # ---------------- BUTTONS ----------------

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="➕ Add to Reading List",
            command=self.save_book
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Update Status",
            command=self.change_status
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="📖 Generate Reading Guide",
            command=self.reading_guide
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="📚 Similar Books",
            command=self.show_similar_books
        ).pack(
            side="left",
            padx=5
        )

        # ---------------- RESULTS ----------------

        results_frame = tk.LabelFrame(
            root,
            text="Results"
        )

        results_frame.pack(
            fill="both",
            padx=20,
            pady=10
        )

        self.results = tk.Text(
            results_frame,
            height=8,
            width=100,
            wrap="word"
        )

        self.results.pack(
            padx=10,
            pady=10
        )

    # ==================================================
    # SEARCH FOR BOOK
    # ==================================================

    def search_book(self):

        search_value = self.search_entry.get().strip()
        search_type = self.search_type.get()

        if not search_value:
            messagebox.showerror(
                "Error",
                "Please enter a title, author, or ISBN."
            )
            return

        try:

            books = search_books(
                search_value,
                search_type
            )

            if not books:
                messagebox.showinfo(
                    "No Results",
                    "No books were found. Try another search."
                )
                return

            # Use the first book returned

            self.current_book = books[0]

            # Display book details

            self.book_title.config(
                text=f"Title: {self.current_book.get('title', 'Unknown')}"
            )

            self.book_author.config(
                text=f"Author: {self.current_book.get('author', 'Unknown')}"
            )

            self.book_isbn.config(
                text=f"ISBN: {self.current_book.get('isbn', 'Not available')}"
            )

            self.book_description.config(
                text=(
                    "Description: "
                    + self.current_book.get(
                        "description",
                        "No description available."
                    )
                )
            )

            # Display cover

            self.display_cover(
                self.current_book.get("cover", "")
            )

            self.results.delete(
                "1.0",
                tk.END
            )

            self.results.insert(
                tk.END,
                "Book found successfully!\n"
            )

        except Exception as error:

            messagebox.showerror(
                "Search Error",
                f"Something went wrong:\n{error}"
            )

    # ==================================================
    # DISPLAY BOOK COVER
    # ==================================================

    def display_cover(self, cover_url):

        if not cover_url:

            self.cover_label.config(
                image="",
                text="No Cover Available"
            )

            return

        try:

            response = requests.get(
                cover_url,
                timeout=10
            )

            response.raise_for_status()

            image_data = Image.open(
                BytesIO(response.content)
            )

            image_data.thumbnail(
                (180, 250)
            )

            self.cover_image = ImageTk.PhotoImage(
                image_data
            )

            self.cover_label.config(
                image=self.cover_image,
                text=""
            )

        except Exception:

            self.cover_label.config(
                image="",
                text="Unable to load cover"
            )

    # ==================================================
    # SAVE BOOK
    # ==================================================

    def save_book(self):

        if not self.current_book:

            messagebox.showwarning(
                "No Book",
                "Please search for a book first."
            )

            return

        try:

            add_book(
                self.current_book
            )

            messagebox.showinfo(
                "Success",
                "Book added to your reading list."
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not save the book:\n{error}"
            )

    # ==================================================
    # CHANGE READING STATUS
    # ==================================================

    def change_status(self):

        if not self.current_book:

            messagebox.showwarning(
                "No Book",
                "Please search for a book first."
            )

            return

        try:

            isbn = self.current_book.get(
                "isbn"
            )

            new_status = self.status.get()

            update_status(
                isbn,
                new_status
            )

            messagebox.showinfo(
                "Success",
                f"Reading status changed to:\n{new_status}"
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not update status:\n{error}"
            )

    # ==================================================
    # GENERATE READING GUIDE
    # ==================================================

    def reading_guide(self):

        if not self.current_book:

            messagebox.showwarning(
                "No Book",
                "Please search for a book first."
            )

            return

        try:

            guide = generate_reading_guide(
                self.current_book
            )

            self.results.delete(
                "1.0",
                tk.END
            )

            self.results.insert(
                tk.END,
                "📖 READING GUIDE\n\n"
            )

            self.results.insert(
                tk.END,
                guide
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not generate reading guide:\n{error}"
            )

    # ==================================================
    # SIMILAR BOOKS
    # ==================================================

    def show_similar_books(self):

        if not self.current_book:

            messagebox.showwarning(
                "No Book",
                "Please search for a book first."
            )

            return

        try:

            similar_books = get_similar_books(
                self.current_book
            )

            self.results.delete(
                "1.0",
                tk.END
            )

            if not similar_books:

                self.results.insert(
                    tk.END,
                    "No similar books found."
                )

                return

            self.results.insert(
                tk.END,
                "📚 SIMILAR BOOKS\n\n"
            )

            for book in similar_books:

                title = book.get(
                    "title",
                    "Unknown"
                )

                author = book.get(
                    "author",
                    "Unknown"
                )

                self.results.insert(
                    tk.END,
                    f"• {title} - {author}\n"
                )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not find similar books:\n{error}"
            )


# ==================================================
# START APPLICATION
# ==================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = BookApp(root)

    root.mainloop()