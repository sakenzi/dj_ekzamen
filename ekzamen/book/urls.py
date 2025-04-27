from django.urls import path
from .views import create_book_view, all_books, all_books_user, update_book_view, delete_book


urlpatterns = [
    path('book', create_book_view, name='book'),
    path('books', all_books, name='books'),
    path('user-books', all_books_user, name='book-user'),
    path('update/<int:pk>/', update_book_view, name='update-book'),
    path('delete/<int:pk>/', delete_book, name='delete-book')
]