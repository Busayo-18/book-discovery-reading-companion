# import necessary libraries
from PIL import ImageOps
import tkinter as tk
from tkinter import ttk, messagebox

# import PIL for image handling
from PIL import Image, ImageTk
import requests
from io import BytesIO

# import custom modules
from api_client import OpenLibraryClient
from reading_list import ReadingListManager
from reading_guide import ReadingGuideGenerator
from recommendations import get_similar_books


# ==================================================
# FOREST GREEN THEME
# ==================================================

COLORS = {
    "primary": "#2E7D32",
    "dark": "#1B5E20",
    "light": "#E8F5E9",
    "background": "#FFFDF5",
    "text": "#263238",
    "white": "#FFFFFF"
}


class BookApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Book Discovery & Reading Companion"
        )

        self.root.geometry("1100x1100")
        self.root.configure(
            bg=COLORS["background"]
        )
        
        # --------------------------------------------------
        # SCROLLABLE APP
        # --------------------------------------------------

        container = tk.Frame(
            self.root,
            bg=COLORS["background"]
        )
        container.pack(
            fill="both",
            expand=True
        )

        canvas = tk.Canvas(
            container,
            bg=COLORS["background"],
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        scrollable_frame = tk.Frame(
            canvas,
            bg=COLORS["background"]
        )

        scrollable_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=scrollable_frame,
            anchor="nw"
        )
        
        def resize_scrollable_frame(event):
            canvas.itemconfig(
                canvas_window,
                width=event.width
            )

        canvas.bind(
            "<Configure>",
            resize_scrollable_frame
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )
        
        def scroll_with_mouse(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas.bind_all(
            "<MouseWheel>",
            scroll_with_mouse
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # --------------------------------------------------
        # OBJECTS
        # --------------------------------------------------

        self.api_client = OpenLibraryClient()

        self.reading_list = ReadingListManager()

        self.guide_generator = ReadingGuideGenerator()

        self.current_book = None

        self.search_results = []

        self.cover_image = None

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title = tk.Label(
            scrollable_frame,
            text="📚 Book Discovery & Reading Companion",
            font=("Arial", 20, "bold"),
            bg=COLORS["background"],
            fg=COLORS["dark"]
        )

        title.pack(pady=15)

        # --------------------------------------------------
        # SEARCH
        # --------------------------------------------------

        search_frame = tk.Frame(
            scrollable_frame,
            bg=COLORS["background"]
        )

        search_frame.pack(pady=10)

        tk.Label(
            search_frame,
            text="Search by:",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=("Arial", 10, "bold")
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.search_type = ttk.Combobox(
            search_frame,
            values=[
                "Title",
                "Author",
                "ISBN"
            ],
            state="readonly",
            width=15
        )

        self.search_type.current(0)

        self.search_type.grid(
            row=0,
            column=1,
            padx=5
        )

        self.search_entry = tk.Entry(
            search_frame,
            width=40,
            bg=COLORS["white"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"]
        )

        self.search_entry.grid(
            row=0,
            column=2,
            padx=5
        )

        # Press Enter to search
        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_book()
        )

        search_button = tk.Button(
            search_frame,
            text="🔎 Search",
            command=self.search_book,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            activebackground=COLORS["dark"],
            activeforeground=COLORS["white"],
            font=("Arial", 10, "bold"),
            padx=10
        )

        search_button.grid(
            row=0,
            column=3,
            padx=5
        )

       self.create_button(
            button_frame,
            "🗑 Remove Book",
            self.remove_book
            ).pack(side="left", padx=5)
        
        # --------------------------------------------------
        # SEARCH RESULTS
        # --------------------------------------------------

        results_list_frame = tk.LabelFrame(
            scrollable_frame,
            text="Search Results",
            padx=10,
            pady=10,
            bg=COLORS["background"],
            fg=COLORS["dark"],
            font=("Arial", 10, "bold")
        )

        results_list_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.book_results = tk.Listbox(
            results_list_frame,
            height=5,
            width=100,
            bg=COLORS["white"],
            fg=COLORS["text"],
            selectbackground=COLORS["primary"],
            selectforeground=COLORS["white"]
        )

        self.book_results.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.book_results.bind(
            "<<ListboxSelect>>",
            self.select_book
        )

        # --------------------------------------------------
        # BOOK DETAILS
        # --------------------------------------------------

        details_frame = tk.LabelFrame(
            scrollable_frame,
            text="Book Details",
            padx=15,
            pady=15,
            bg=COLORS["background"],
            fg=COLORS["dark"],
            font=("Arial", 11, "bold")
        )

        details_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # --------------------------------------------------
        # COVER
        # --------------------------------------------------

        self.cover_label = tk.Label(
            details_frame,
            text="Book Cover",
            width=25,
            height=20,
            bg=COLORS["light"],
            fg=COLORS["text"]
        )

        self.cover_label.pack(
            side="left",
            padx=20
        )

        # --------------------------------------------------
        # BOOK INFORMATION
        # --------------------------------------------------

        info_frame = tk.Frame(
            details_frame,
            bg=COLORS["background"]
        )

        info_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.book_title = tk.Label(
            info_frame,
            text="Title:",
            font=("Arial", 13, "bold"),
            anchor="w",
            bg=COLORS["background"],
            fg=COLORS["dark"]
        )

        self.book_title.pack(
            anchor="w",
            pady=5
        )

        self.book_author = tk.Label(
            info_frame,
            text="Author:",
            anchor="w",
            bg=COLORS["background"],
            fg=COLORS["text"]
        )

        self.book_author.pack(
            anchor="w",
            pady=5
        )

        self.book_isbn = tk.Label(
            info_frame,
            text="ISBN:",
            anchor="w",
            bg=COLORS["background"],
            fg=COLORS["text"]
        )

        self.book_isbn.pack(
            anchor="w",
            pady=5
        )

        self.book_year = tk.Label(
            info_frame,
            text="First Publication Year:",
            anchor="w",
            bg=COLORS["background"],
            fg=COLORS["text"]
        )

        self.book_year.pack(
            anchor="w",
            pady=5
        )

        self.book_pages = tk.Label(
            info_frame,
            text="Page Count:",
            anchor="w",
            bg=COLORS["background"],
            fg=COLORS["text"]
        )

        self.book_pages.pack(
            anchor="w",
            pady=5
        )

        self.book_description = tk.Label(
            info_frame,
            text="Subjects:",
            wraplength=600,
            justify="left",
            anchor="nw",
            bg=COLORS["background"],
            fg=COLORS["text"]
        )

        self.book_description.pack(
            anchor="w",
            pady=5
        )

        # --------------------------------------------------
        # READING STATUS
        # --------------------------------------------------

        status_frame = tk.Frame(
            scrollable_frame,
            bg=COLORS["background"]
        )

        status_frame.pack(
            pady=10
        )

        tk.Label(
            status_frame,
            text="Reading Status:",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=("Arial", 10, "bold")
        ).pack(
            side="left",
            padx=5
        )

        self.status = ttk.Combobox(
            status_frame,
            values=[
                "Want to Read",
                "Reading",
                "Finished"
            ],
            state="readonly",
            width=20
        )

        self.status.current(0)

        self.status.pack(
            side="left",
            padx=5
        )

        # --------------------------------------------------
        # BUTTONS
        # --------------------------------------------------

        button_frame = tk.Frame(
            scrollable_frame,
            bg=COLORS["background"]
        )

        button_frame.pack(
            pady=10
        )

        self.create_button(
            button_frame,
            "➕ Add to Reading List",
            self.save_book
        ).pack(
            side="left",
            padx=5
        )

        self.create_button(
            button_frame,
            "Update Status",
            self.change_status
        ).pack(
            side="left",
            padx=5
        )

        self.create_button(
            button_frame,
            "📖 Generate Reading Guide",
            self.reading_guide
        ).pack(
            side="left",
            padx=5
        )

        self.create_button(
            button_frame,
            "📚 Similar Books",
            self.show_similar_books
        ).pack(
            side="left",
            padx=5
        )
        
        self.create_button(
            button_frame,
            "📋 My Reading List",
            self.view_reading_list
            ).pack(side="left", padx=5)

        # --------------------------------------------------
        # RESULTS
        # --------------------------------------------------

        results_frame = tk.LabelFrame(
            scrollable_frame,
            text="Results",
            bg=COLORS["background"],
            fg=COLORS["dark"],
            font=("Arial", 10, "bold")
        )

        results_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.results = tk.Text(
            results_frame,
            height=12,
            wrap="word",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=("Arial", 10)
        )

        self.results.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # ==================================================
    # CREATE BUTTON
    # ==================================================

    def create_button(self, parent, text, command):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            activebackground=COLORS["dark"],
            activeforeground=COLORS["white"],
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )

    # ==================================================
    # SEARCH FOR BOOKS
    # ==================================================

    def search_book(self):

        search_value = (
            self.search_entry.get().strip()
        )

        search_type = self.search_type.get()

        if not search_value:

            messagebox.showerror(
                "Error",
                "Please enter a title, author, or ISBN."
            )

            return

        try:

            if search_type == "Title":

                books = self.api_client.search_by_title(
                    search_value
                )

            elif search_type == "Author":

                books = self.api_client.search_by_author(
                    search_value
                )

            elif search_type == "ISBN":

                books = self.api_client.search_by_isbn(
                    search_value
                )

            else:

                books = []

            if not books:

                messagebox.showinfo(
                    "No Results",
                    "No books were found. Try another search."
                )

                return

            # Store search results
            self.search_results = books

            # Clear previous results
            self.book_results.delete(
                0,
                tk.END
            )

            # Add books to results list
            for number, book in enumerate(
                books,
                start=1
            ):

                authors = (
                    ", ".join(book.authors)
                    if book.authors
                    else "Unknown author"
                )

                self.book_results.insert(
                    tk.END,
                    f"{number}. {book.title} — {authors}"
                )

            # Automatically select first book
            self.book_results.selection_set(0)

            self.display_book(
                books[0]
            )

        except Exception as error:

            messagebox.showerror(
                "Search Error",
                f"Something went wrong:\n{error}"
            )

    # ==================================================
    # SELECT BOOK FROM SEARCH RESULTS
    # ==================================================

    def select_book(self, event):

        selection = (
            self.book_results.curselection()
        )

        if not selection:
            return

        index = selection[0]

        book = self.search_results[index]

        self.display_book(book)

    # ==================================================
    # DISPLAY BOOK
    # ==================================================

    def display_book(self, book):

        self.current_book = book

        title = (
            book.title
            if book.title
            else "Unknown"
        )

        self.book_title.config(
            text=f"Title: {title}"
        )

        authors= (
            ", ".join(book.authors)
            if book.authors
            else "Unknown"
        )

        self.book_author.config(
            text=f"Author: {authors}"
        )

        isbn = (
            book.isbn
            if book.isbn
            else "Not available"
        )

        self.book_isbn.config(
            text=f"ISBN: {isbn}"
        )

        year = (
            book.first_publication_year
            if book.first_publication_year
            else "Not available"
        )

        self.book_year.config(
            text=f"First Publication Year: {year}"
        )

        page_count = (
            book.pagecount
            if book.pagecount
            else "Not available"
        )

        self.book_pages.config(
            text=f"Page Count: {page_count}"
        )

        subjects = (
            ", ".join(book.subjects[:5])
            if book.subjects
            else "Not available"
        )

        self.book_description.config(
            text=f"Subjects: {subjects}"
        )

        self.display_cover(
            book.cover_url
        )

        self.results.delete(
            "1.0",
            tk.END
        )

        self.results.insert(
            tk.END,
            "Book selected successfully!\n"
        )

    # ==================================================
    # DISPLAY COVER
    # ==================================================

    def display_cover(self, cover_url):

        if not cover_url:
            self.cover_label.config(
                image="",
                text="No Cover Available",
                width=25,
                height=20
            )
            return

        try:
            response = requests.get(cover_url, timeout=10)
            response.raise_for_status()

            image_data = Image.open(BytesIO(response.content))
            image_data = ImageOps.contain(image_data, (300, 400))

            self.cover_image = ImageTk.PhotoImage(image_data)

            self.cover_label.config(
                image=self.cover_image,
                text="",
                width=0,
                height=0
            )

        except Exception:
            self.cover_label.config(
                image="",
                text="Unable to load cover",
                width=25,
                height=20
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

            self.reading_list.add_book(
                self.current_book
            )

            self.reading_list.save_list()

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

            isbn = self.current_book.isbn

            new_status = self.status.get()

            self.reading_list.update_status(
                isbn,
                new_status
            )

            self.reading_list.save_list()

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

            updated_book = (
                self.guide_generator.generate_guide(
                    self.current_book
                )
            )

            self.results.delete(
                "1.0",
                tk.END
            )

            if not updated_book:

                self.results.insert(
                    tk.END,
                    "Could not generate a reading guide."
                )

                return

            self.results.insert(
                tk.END,
                "📖 READING GUIDE\n\n"
            )

            self.results.insert(
                tk.END,
                f"Summary:\n"
                f"{updated_book.summary}\n\n"
            )

            self.results.insert(
                tk.END,
                f"Reading Level:\n"
                f"{updated_book.reading_level}\n\n"
            )

            self.results.insert(
                tk.END,
                "Discussion Questions:\n"
            )

            for number, question in enumerate(
                updated_book.discussion_questions,
                start=1
            ):

                self.results.insert(
                    tk.END,
                    f"{number}. {question}\n"
                )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not generate reading guide:\n{error}"
            )

    # ==================================================
    # SHOW SIMILAR BOOKS
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
                self.current_book,
                self.api_client,
                self.reading_list.books
            )

            self.results.delete(
                "1.0",
                tk.END
            )

            if not similar_books:

                self.results.insert(
                    tk.END,
                    "No similar books found in your "
                    "reading list.\n\n"
                    "Add more books with similar authors "
                    "or subjects to get recommendations."
                )

                return

            self.results.insert(
                tk.END,
                "📚 SIMILAR BOOKS\n\n"
            )

            for book in similar_books:

                authors = (
                    ", ".join(book.authors)
                    if book.authors
                    else "Unknown author"
                )

                self.results.insert(
                    tk.END,
                    f"• {book.title} - {authors}\n"
                )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not find similar books:\n{error}"
            )
            
    
    # ==================================================
    # VIEW READING LIST
    # ==================================================        
    def view_reading_list(self):

        self.results.delete("1.0", tk.END)

        if not self.reading_list.books:
            self.results.insert(tk.END, "Your reading list is empty.")
            return

        self.results.insert(tk.END, "📋 MY READING LIST\n\n")

        for number, book in enumerate(self.reading_list.books, start=1):
            authors = ", ".join(book.authors) if book.authors else "Unknown author"

            self.results.insert(
                tk.END,
                f"{number}. {book.title} — {authors}\n"
                f"   Status: {book.status}\n\n"
            )
    
    # ==================================================
    # REMOVE BOOK
    # ==================================================
    
    def remove_book(self):
    
        if not self.current_book:
            messagebox.showwarning("No Book", "Please search for a book first.")
            return
    
        confirm = messagebox.askyesno(
            "Remove Book",
            f'Remove "{self.current_book.title}" from your reading list?'
        )
    
        if not confirm:
            return
    
        try:
            isbn = self.current_book.isbn
            title = self.current_book.title
    
            self.reading_list.remove_book(isbn)
            self.reading_list.save_list()
    
            messagebox.showinfo("Removed", f'"{title}" has been removed from your reading list.')
    
        except Exception as error:
            messagebox.showerror("Error", f"Could not remove the book:\n{error}")


# ==================================================
# START APPLICATION
# ==================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = BookApp(root)

    root.mainloop()
