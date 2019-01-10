from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book
from django.utils import timezone
# Create your views here.
def home(request):
    books = Book.objects
    return render(request, 'books/home.html', {'books':books})

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            book = Book()
            book.title = request.POST['title']
            book.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                book.url = request.POST['url']
            else:
                book.url = 'http://' + request.POST['url']
            book.icon = request.FILES['icon']
            book.image = request.FILES['image']
            book.pub_date = timezone.datetime.now()
            book.hunter = request.user
            book.save()
            return redirect('/books/' + str(book.id))
        else:
            return render(request,'books/create.html',{'error':'All field are required'})

    else:
        return render(request,'books/create.html')

def detail(request, book_id):
    book = get_object_or_404(Book, pk = book_id)
    return render(request, 'books/detail.html', {'book':book})

@login_required(login_url="/accounts/signup")
def buy(request, book_id):
    if request.method == 'POST':
        print("debug")
        book = get_object_or_404(Book, pk = book_id)
        book.votes_total += 1
        book.save()
        return redirect('/books/' + str(book.id))
