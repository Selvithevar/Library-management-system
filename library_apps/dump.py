import requests
from sqlalchemy import create_engine, exc

def connection():
    try:
        conn = create_engine('mysql+pymysql://root:root@localhost/library_management_system')
        conn = conn.connect()
    except exc.SQLAlchemyError as e:
        print(e)

    return conn

conn = connection()


# Define the API URL
api_url = "https://frappe.io/api/method/frappe-library"

# Define query parameters to fetch 20 books with a specific title
params = {
    "page": 2,
    "title": "and",
}

# Make an HTTP GET request to the API
response = requests.get(api_url, params=params)
# print(response)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Assuming data is a list of books, you can iterate through them
    for book in data["message"]:
        # Extract book information
        book_id = book["bookID"]
        title = book["title"]
        authors = book["authors"]
        isbn = book["isbn"]
        publication_date = book["publication_date"]
        publisher = book["publisher"]
        print(book)


        # conn.execute(f"INSERT into library_app_book (book_id,title,authors,isbn,publication_date,publisher) VALUES ('{book_id}','{title}','{authors}','{isbn}','{publication_date}','{publisher}')")
        # conn.dispose()

        # Create a book record in your Django model
        # Assuming you have a Book model defined
        from library_apps.models import Book

        Book.objects.create(
            book_id=book_id,
            title=title,
            authors=authors,
            isbn=isbn,
            publication_date=publication_date,
            publisher=publisher,
        )

        # You can add more fields as needed

    print("Books imported successfully.")
else:
    print("Failed to fetch books from the API. Status code:", response.status_code)
