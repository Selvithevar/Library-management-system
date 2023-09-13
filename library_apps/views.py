import requests
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

def register(request):
    form = CustomUserForm()
    if request.method=='POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'register.html',{'form':form})

# <----Login page------>

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username,password=password)

            if user is not None:
                form = LoginForm()
                auth.login(request,user)
                return redirect('add_book')
    context = {'form':form}
    return render(request,'login.html',context=context)


def import_books(request):
    if request.method == 'POST':
        # Get the number of books to import from the form
        num_books_to_import = int(request.POST.get('num_books', 20))  # Default to 20 books

        # Define the Frappe API URL
        frappe_api_url = "https://frappe.io/api/method/frappe-library"

        # Define parameters for the API request
        params = {
            "page": 1,  # Specify the page number if needed
            "title": "Harry Potter",  # Specify the title or other search parameters
        }

        try:
            # Make a GET request to the Frappe API
            response = requests.get(frappe_api_url, params=params)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Process and create book records
                for book_info in data.get("message", [])[:num_books_to_import]:
                    title = book_info["title"]
                    author = book_info["authors"]
                    isbn = book_info["isbn"]

                    Book.objects.create(title=title, author=author, isbn=isbn)

                return redirect('book_list')  # Redirect to the book list page
            else:
                return render(request, 'import_books.html', {'error_message': f"Failed to import books. Status code: {response.status_code}"})
        except Exception as e:
            return render(request, 'import_books.html', {'error_message': f"An error occurred: {str(e)}"})

    return render(request, 'import_books.html')



def book_list(request):
    books = Book.objects.all()
    return render(request,'book_lists.html',{'books':books})

# View for adding a new book
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        stock = request.POST['stock']
        Book.objects.create(title=title, author=author, isbn=isbn, stock=stock)
        return redirect('book_list')
    return render(request, 'add_book.html')

def updatebook(request,id):
    book = Book.objects.get(id=id)
    form = ImportBooksForm(instance=book)
    if request.method == 'POST':
        form = ImportBooksForm(request.POST,instance=book)
        if form.is_valid():
            form.save()
            return redirect('/book_list/')
    context = {'form':form}
    return render(request,'update_book.html',context=context)

def deletebook(request,id):
    book = Book.objects.get(id=id)    
    if request.method == 'POST':
        book.delete()
        return redirect('/book_list')
    context = {'object':book}
    return render(request,'delete_book.html',context=context)

# View for listing all members
def member_list(request):
    members = Member.objects.all()
    return render(request, 'member_list.html', {'members': members})

# View for adding a new member
def add_member(request):
    if request.method == 'POST':
        name = request.POST['name']
        outstanding_debt = request.POST['outstanding_debt']
        Member.objects.create(name=name,outstanding_debt=outstanding_debt)
        return redirect('member_list')
    return render(request, 'add_member.html')

def updatemember(request,id):
    book = Member.objects.get(id=id)
    form = updateMemberform(instance=book)
    if request.method == 'POST':
        form = updateMemberform(request.POST,instance=book)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    context = {'form':form}
    return render(request,'update_member.html',context=context)

def deletemember(request,id):
    book = Member.objects.get(id=id)    
    if request.method == 'POST':
        book.delete()
        return redirect('member_list')
    context = {'object':book}
    return render(request,'delete_member.html',context=context)

def transaction_lists(request):
    transactions = Transaction.objects.all()
    return render(request,'transaction_lists.html',{'transactions':transactions})

# View for issuing a book to a member
def issue_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == 'POST':
        member_id = request.POST['member']
        member = Member.objects.get(pk=member_id)
        issue_date = request.POST['issue_date']
        return_date = request.POST['return_date']
        Transaction.objects.create(book=book, member=member,issue_date=issue_date,return_date=return_date, status='issued')
        # book.stock -= 1
        # book.save()
        return redirect('/transaction_lists')
    members = Member.objects.all()
    return render(request, 'issue_book.html', {'book': book, 'members': members})

# View for returning a book from a member
def return_book(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    if request.method == 'POST':
        days_overdue = int(request.POST['days_overdue'])
        if days_overdue > 0:
            # Calculate rent fee
            rent_fee = days_overdue * 10  # Rs. 10 per day
            transaction.fee = rent_fee
        transaction.status = 'returned'
        transaction.save()
        # book = transaction.book
        # book.stock += 1
        # book.save()
        return redirect('transaction_lists')
    return render(request, 'return_book.html', {'transaction': transaction})

# View for searching for books by name and author
def search_books(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        books = []
    return render(request, 'search_books.html', {'books': books})

def logout(request):
    auth.logout(request)
    return redirect('login')