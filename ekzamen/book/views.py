from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateBookForm
from .models import Book
from django.contrib.auth.decorators import login_required


# Create your views here.
def create_book_view(request):
    if request.method == 'POST':
        form = CreateBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('home')
    
    else:
        form = CreateBookForm()
    return render(request, 'book/create_book.html', {'form': form})

def all_books(request):
    books = Book.objects.all()
    return render(request, 'book/book_list.html', {'books': books})

def all_books_user(request):
    books = Book.objects.all().filter(user=request.user)
    return render(request, 'book/book_list.html', {'books': books})

@login_required
def update_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)

    if request.method == 'POST':
        form = CreateBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = CreateBookForm(instance=book)

    return render(request, 'book/update_book.html', {'form': form})

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    
    return render(request, 'book/delete_book.html', {'book': book})
