----BOOK DISCOVERY READING COMPANION----
A Python desktop application for discovering books, viewing book information, managing a personal reading list, generating AI-powered reading guides, and finding similar books.

-----Features-----
1.Search books by title, author, or ISBN

2.Display multiple search results in a selectable list

3.View title, authors, ISBN, publication year, page count, subjects, and cover

4.Add and remove books from a reading list

5.Set status to Want to Read, Reading, or Finished

6. View your full saved reading list inside the app

7.Save and load the reading list using JSON

8.Generate AI reading guides with Google Gemini

9.Recommend similar books using shared authors and subjects — checking your reading list first, then searching Open Library directly

10.Press Enter to search

10.Handles missing data and common API errors

-----Technologies-----
Python
Tkinter
Open Library API
Google Gemini API
Requests
Pillow
python-dotenv
JSON
Git/GitHub

------Project Structure-----

book-discovery-reading-companion/
├── app.py
├── api_client.py
├── models.py
├── reading_list.py
├── reading_guide.py
├── recommendations.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

-app.py
Main Tkinter application. Builds the whole interface (search bar, results list, book details, reading list, buttons) and connects every other module together.

-api_client.py
Contains OpenLibraryClient, which searches Open Library by title, author, ISBN, or subject, and converts each result into a Book object. Requests a fixed set of fields from the API so results are as complete as possible, and returns a list of books rather than just one

-models.py
Contains the Book class — the shared shape every other module builds around. Stores a book's details plus its reading status, AI summary, reading level, and discussion questions, and can convert itself to/from a dictionary for saving to JSON.

-reading_list.py
Contains ReadingListManager, which adds/removes books (matched by ISBN), updates reading status, and saves/loads the whole list to reading_list.json — including handling a missing or corrupted file without crashing

-reading_guide.py
Contains ReadingGuideGenerator, which sends a book's details to Google Gemini and parses the reply into a summary, reading level, and five discussion questions, stored directly on the Book object.

-recommendations.py
Finds similar books using shared authors and subjects.Contains get_similar_books, which first checks the user's own reading list for books sharing an author or subject, then also searches Open Library directly by the book's top subject — so recommendations still work even for a brand-new user with an empty list.

------Installation-----
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd book-discovery-reading-companion
2. Create a virtual environment
Windows PowerShell:

python -m venv venv
venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
Expected dependencies:

requests
python-dotenv
google-genai
Pillow
Gemini API Configuration
Create a .env file in the project root:

GEMINI_API_KEY=your_real_api_key_here
Use .env.example as the template.

Never commit .env to GitHub. It should be listed in .gitignore.

-----Running the Application----
python app.py
The Tkinter desktop window will open.

-----How to Use-----
1. Search:Select Title, Author, or ISBN.

2. Enter a search term.

3. Click Search or press Enter.

4. Select a result from the results list.

5. The selected book's details will appear.

------Reading List-----
1.Search for a book.

2.Select it.

3.Click Add to Reading List.

4. Choose or update its reading status.

5.The list is stored locally in reading_list.json.

6. Click My Reading List at any time to view every saved book and its status.

------Available statuses-----
Want to Read
Reading
Finished

------Reading Guide------
Select a book and click Generate Reading Guide.
Gemini generates:Summary, Reading level, Discussion/comprehension questions
A valid Gemini API key and internet connection are required.

------Similar Books-----
Select a book and click Similar Books. The recommendation system first checks books already in your reading list (shared authors, shared subjects), then searches Open Library directly using the book's top subject — so you'll get recommendations even if your reading list is empty or small


------Data Storage------
The reading list is stored in reading_list.json

The application loads the file when it starts and saves changes locally.

If the file does not exist, the application starts with an empty list.

------API Usage------
Open Library
Open Library provides the book metadata used by the application, including titles, authors, publication years, subjects, page counts, ISBNs, and cover information.

Google Gemini
Gemini is used only for the AI reading-guide feature.

The API key is loaded from the .env environment file.

------Error Handling------
The application handles situations such as:Empty searches, No search results, Open Library request failures, Invalid API responses, Missing book information,Missing covers, Missing reading-list files, Invalid or corrupted JSON, Invalid reading statuses, Gemini/API failures

------Object-Oriented Design------
The project separates responsibilities into classes:

Book — represents a book

OpenLibraryClient — communicates with Open Library

ReadingListManager — manages saved books

ReadingGuideGenerator — communicates with Gemini

This structure makes the application easier to test, maintain, and extend.

Application Flow
User
  |
  v
Tkinter GUI (app.py)
  |
  +--> OpenLibraryClient --> Open Library API
  |
  +--> ReadingListManager --> reading_list.json
  |
  +--> ReadingGuideGenerator --> Gemini API
  |
  +--> Recommendation System

-----Troubleshooting-----
ModuleNotFoundError
Run:
pip install -r requirements.txt
Gemini is not working

Check that:
.env exists
GEMINI_API_KEY is correctly set
the API key is valid
google-genai is installed
internet access is available

------Cover is missing------
Some Open Library records do not contain a cover. The application displays a fallback when no cover is available.

No similar books
Recommendations check your reading list first, then Open Library by subject — a book with no listed subjects may return fewer results.

Git Collaboration
The project uses feature branches before integration.

Example branches:
main
Group-leader-integration
member2-api
member3-book-model
member4-reading-list
member5-reading-guide
member6-ui



------Future Improvements-------

More advanced recommendations

Sorting and filtering

CSV export

Dark mode

User accounts and cloud storage

Package the desktop application as a Windows .exe

Create a web version of the application

------License-------
This project was developed as a group project for Python Advanced as NITDA Interns.
